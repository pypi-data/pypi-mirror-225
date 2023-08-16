#
# This python script gives an example on using JAX and PyBORG together
#
import jax
import numpy as np
import borg

cons = borg.console()

myprint=lambda x: cons.print_std(x) if type(x) == str else cons.print_std(repr(x))
myprint("Hello!")

@jax.jit
def jax_func(rho):
   return rho**2

class MyModel(borg.forward.BaseForwardModel):
   def __init__(self, box):
     myprint("Start forward model")
     super().__init__(box, box)

   def getPreferredInput(self):
     return borg.forward.PREFERRED_REAL

   def getPreferredOutput(self):
     return borg.forward.PREFERRED_REAL

   def forwardModel_v2_impl(self, input_array):
     # Save the input data in a jax array (i.e. upload to accelerator)
     self.save = jax.numpy.array(input_array)
 
   def getDensityFinal_impl(self, output_array):
     # Run forward, and save the AG function
     fwd, self.ag_fun = jax.vjp(jax_func, self.save)
     output_array[:] = fwd

   def adjointModel_v2_impl(self, input_ag):
     # Save the ag vector
     self.ag = input_ag
   
   def getAdjointModel_impl(self, output_ag):
     # Evaluate the new function with ag_fun
     out_ag, = self.ag_fun(self.ag)
     output_ag[:] = out_ag

def build_gravity_model(box):
  chain = borg.forward.ChainForwardModel(box)
  chain.addModel(borg.forward.models.Primordial(box, 1.0))
  chain.addModel(borg.forward.models.EisensteinHu(box))
  chain.addModel(borg.forward.models.BorgLpt(box, box, ai=1.0))
  chain.addModel(MyModel(box))
  return chain


if __name__ == "__main__":
  box = borg.forward.BoxModel()
  cpar = borg.cosmo.CosmologicalParameters()

  chain = build_gravity_model(box)
  chain.setCosmoParams(cpar)

  s_hat = np.fft.rfftn(np.random.randn(*box.N)/np.sqrt(box.N[0]**3))

  myprint(np.var(s_hat))

  chain.forwardModel_v2(s_hat)
  rho = np.zeros(chain.getOutputBoxModel().N)
  chain.getDensityFinal(rho)


  ag = 2*rho
  chain.adjointModel_v2(ag)
  chain.getAdjointModel(ag)
