HMCDensitySampler::HamiltonianType HMCDensitySampler::computeHamiltonian_Prior(
    MarkovState &state, CArrayRef const &s_array) {
  auto s_w = fwrap(s_array);
  auto r = std::real(s_w);
  auto i = std::imag(s_w);
  double Eprior = (r*r+i*i).sum() / (0.5);

  comm->all_reduce_t(MPI_IN_PLACE, &Eprior, 1, MPI_SUM);

  return Eprior*0.5;
}

void HMCDensitySampler::computeGradientPsi_Prior(
    MarkovState &state, CArrayRef const &s, CArrayRef &grad_array) {
  ConsoleContext<LOG_DEBUG> ctx("gradient psi prior");
  fwrap(grad_array) = fwrap(s)*2.0;
}
