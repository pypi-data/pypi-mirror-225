#+
#   ARES/HADES/BORG Package -- ./scripts/misc/check_bias.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import read_all_h5
from pylab import *

n=[]
b0=[]
b1=[]
b2=[]
b3=[]
b4=[]
b5=[]
b6=[]
b7=[]
b8=[]
b9=[]
b10=[]
b11=[]
b12=[]
b13=[]
b14=[]
b15=[]


rho_g0=[]
rho_g1=[]
rho_g2=[]
rho_g3=[]
rho_g4=[]
rho_g5=[]
rho_g6=[]
rho_g7=[]
rho_g8=[]
rho_g9=[]
rho_g10=[]
rho_g11=[]
rho_g12=[]
rho_g13=[]
rho_g14=[]
rho_g15=[]


eps_g0=[]
eps_g1=[]
eps_g2=[]
eps_g3=[]
eps_g4=[]
eps_g5=[]
eps_g6=[]
eps_g7=[]
eps_g8=[]
eps_g9=[]
eps_g10=[]
eps_g11=[]
eps_g12=[]
eps_g13=[]
eps_g14=[]
eps_g15=[]


n0=[]
n1=[]
n2=[]
n3=[]
n4=[]
n5=[]
n6=[]
n7=[]
n8=[]
n9=[]
n10=[]
n11=[]
n12=[]
n13=[]
n14=[]
n15=[]


accept=[]

i=0
#while True:



for l in range(0,440,1):
  a = \
   read_all_h5.read_all_h5("mcmc_%d.h5" % l)
  try:
    n0.append(a.scalars.galaxy_nmean_0)
    n1.append(a.scalars.galaxy_nmean_1)
    n2.append(a.scalars.galaxy_nmean_2)
    n3.append(a.scalars.galaxy_nmean_3)
    n4.append(a.scalars.galaxy_nmean_4)
    n5.append(a.scalars.galaxy_nmean_5)
    n6.append(a.scalars.galaxy_nmean_6)
    n7.append(a.scalars.galaxy_nmean_7)
    n8.append(a.scalars.galaxy_nmean_8)
    n9.append(a.scalars.galaxy_nmean_9)
    n10.append(a.scalars.galaxy_nmean_10)
    n11.append(a.scalars.galaxy_nmean_11)
    n12.append(a.scalars.galaxy_nmean_12)
    n13.append(a.scalars.galaxy_nmean_13)
    n14.append(a.scalars.galaxy_nmean_14)
    n15.append(a.scalars.galaxy_nmean_15)
    
    
    b0.append(a.scalars.galaxy_bias_0)
    b1.append(a.scalars.galaxy_bias_1)
    b2.append(a.scalars.galaxy_bias_2)
    b3.append(a.scalars.galaxy_bias_3)
    b4.append(a.scalars.galaxy_bias_4)
    b5.append(a.scalars.galaxy_bias_5)
    b6.append(a.scalars.galaxy_bias_6)
    b7.append(a.scalars.galaxy_bias_7)
    b8.append(a.scalars.galaxy_bias_8)
    b9.append(a.scalars.galaxy_bias_9)
    b10.append(a.scalars.galaxy_bias_10)
    b11.append(a.scalars.galaxy_bias_11)
    b12.append(a.scalars.galaxy_bias_12)
    b13.append(a.scalars.galaxy_bias_13)
    b14.append(a.scalars.galaxy_bias_14)
    b15.append(a.scalars.galaxy_bias_15)
    
    rho_g0.append(a.scalars.galaxy_rho_g_0)
    rho_g1.append(a.scalars.galaxy_rho_g_1)
    rho_g2.append(a.scalars.galaxy_rho_g_2)
    rho_g3.append(a.scalars.galaxy_rho_g_3)
    rho_g4.append(a.scalars.galaxy_rho_g_4)
    rho_g5.append(a.scalars.galaxy_rho_g_5)
    rho_g6.append(a.scalars.galaxy_rho_g_6)
    rho_g7.append(a.scalars.galaxy_rho_g_7)
    rho_g8.append(a.scalars.galaxy_rho_g_8)
    rho_g9.append(a.scalars.galaxy_rho_g_9)
    rho_g10.append(a.scalars.galaxy_rho_g_10)
    rho_g11.append(a.scalars.galaxy_rho_g_11)
    rho_g12.append(a.scalars.galaxy_rho_g_12)
    rho_g13.append(a.scalars.galaxy_rho_g_13)
    rho_g14.append(a.scalars.galaxy_rho_g_14)
    rho_g15.append(a.scalars.galaxy_rho_g_15)
    
    eps_g0.append(a.scalars.galaxy_eps_g_0)
    eps_g1.append(a.scalars.galaxy_eps_g_1)
    eps_g2.append(a.scalars.galaxy_eps_g_2)
    eps_g3.append(a.scalars.galaxy_eps_g_3)
    eps_g4.append(a.scalars.galaxy_eps_g_4)
    eps_g5.append(a.scalars.galaxy_eps_g_5)
    eps_g6.append(a.scalars.galaxy_eps_g_6)
    eps_g7.append(a.scalars.galaxy_eps_g_7)
    eps_g8.append(a.scalars.galaxy_eps_g_8)
    eps_g9.append(a.scalars.galaxy_eps_g_9)
    eps_g10.append(a.scalars.galaxy_eps_g_10)
    eps_g11.append(a.scalars.galaxy_eps_g_11)
    eps_g12.append(a.scalars.galaxy_eps_g_12)
    eps_g13.append(a.scalars.galaxy_eps_g_13)
    eps_g14.append(a.scalars.galaxy_eps_g_14)
    eps_g15.append(a.scalars.galaxy_eps_g_14)
    
    accept.append(a.scalars.hades_accept_count)
    print l
  except AttributeError:
    break
  i += 1

rate =np.cumsum(np.array(accept))
norm =np.cumsum(np.ones(len(accept)))

plt.plot(rate/norm)
plt.show()

print 

plt.plot(b0,label=str(0))
plt.plot(b1,label=str(1))
plt.plot(b2,label=str(2))
plt.plot(b3,label=str(3))
plt.plot(b4,label=str(4))
plt.plot(b5,label=str(5))
plt.plot(b6,label=str(6))
plt.plot(b7,label=str(7))
plt.plot(b8,label=str(0))
plt.plot(b9,label=str(1))
plt.plot(b10,label=str(2))
plt.plot(b11,label=str(3))
plt.plot(b12,label=str(4))
plt.plot(b13,label=str(5))
plt.plot(b14,label=str(6))
plt.plot(b15,label=str(7))

legend()
plt.savefig('check_bias.png')
plt.show()


plt.plot(np.log10(rho_g0),label=str(0))
plt.plot(np.log10(rho_g1),label=str(1))
plt.plot(np.log10(rho_g2),label=str(2))
plt.plot(np.log10(rho_g3),label=str(3))
plt.plot(np.log10(rho_g4),label=str(4))
plt.plot(np.log10(rho_g5),label=str(5))
plt.plot(np.log10(rho_g6),label=str(6))
plt.plot(np.log10(rho_g7),label=str(7))
plt.plot(np.log10(rho_g8),label=str(0))
plt.plot(np.log10(rho_g9),label=str(1))
plt.plot(np.log10(rho_g10),label=str(2))
plt.plot(np.log10(rho_g11),label=str(3))
plt.plot(np.log10(rho_g12),label=str(4))
plt.plot(np.log10(rho_g13),label=str(5))
plt.plot(np.log10(rho_g14),label=str(6))
plt.plot(np.log10(rho_g15),label=str(7))
legend()
plt.savefig('check_rho_g.png')
plt.show()



x=np.arange(600)*0.04+1e-12

y0=n0[-1]*x**b0[-1]*np.exp(-rho_g0[-1]*x**(-eps_g0[-1]))
y1=n1[-1]*x**b1[-1]*np.exp(-rho_g1[-1]*x**(-eps_g1[-1]))
y2=n2[-1]*x**b2[-1]*np.exp(-rho_g2[-1]*x**(-eps_g2[-1]))
y3=n3[-1]*x**b3[-1]*np.exp(-rho_g3[-1]*x**(-eps_g3[-1]))
y4=n4[-1]*x**b4[-1]*np.exp(-rho_g4[-1]*x**(-eps_g4[-1]))
y5=n5[-1]*x**b5[-1]*np.exp(-rho_g5[-1]*x**(-eps_g5[-1]))
y6=n6[-1]*x**b6[-1]*np.exp(-rho_g6[-1]*x**(-eps_g6[-1]))
y7=n7[-1]*x**b7[-1]*np.exp(-rho_g7[-1]*x**(-eps_g7[-1]))
y8=n8[-1]*x**b8[-1]*np.exp(-rho_g8[-1]*x**(-eps_g8[-1]))
y9=n9[-1]*x**b9[-1]*np.exp(-rho_g9[-1]*x**(-eps_g9[-1]))
y10=n10[-1]*x**b10[-1]*np.exp(-rho_g10[-1]*x**(-eps_g10[-1]))
y11=n11[-1]*x**b11[-1]*np.exp(-rho_g11[-1]*x**(-eps_g11[-1]))
y12=n12[-1]*x**b12[-1]*np.exp(-rho_g12[-1]*x**(-eps_g12[-1]))
y13=n13[-1]*x**b13[-1]*np.exp(-rho_g13[-1]*x**(-eps_g13[-1]))
y14=n14[-1]*x**b14[-1]*np.exp(-rho_g14[-1]*x**(-eps_g14[-1]))
y15=n15[-1]*x**b15[-1]*np.exp(-rho_g15[-1]*x**(-eps_g15[-1]))


plt.plot(x,np.log(y0),label=str(0),color='red')
plt.plot(x,np.log(y1),label=str(1),color='blue')
plt.plot(x,np.log(y2),label=str(2),color='green')
plt.plot(x,np.log(y3),label=str(3),color='orange')
plt.plot(x,np.log(y4),label=str(4),color='yellow')
plt.plot(x,np.log(y5),label=str(5),color='black')
plt.plot(x,np.log(y6),label=str(6),color='gray')
plt.plot(x,np.log(y7),label=str(7),color='magenta')
plt.plot(x,np.log(y8),label=str(0),color='red')
plt.plot(x,np.log(y9),label=str(1),color='blue')
plt.plot(x,np.log(y10),label=str(2),color='green')
plt.plot(x,np.log(y11),label=str(3),color='orange')
plt.plot(x,np.log(y12),label=str(4),color='yellow')
plt.plot(x,np.log(y13),label=str(5),color='black')
plt.plot(x,np.log(y14),label=str(6),color='gray')
plt.plot(x,np.log(y15),label=str(7),color='magenta')


plt.plot(x,np.log(x),label=str(99))
plt.ylim([-8,5])
legend(loc='lower right', shadow=True)
#plt.show()
gcf().savefig("check_bias.png")








