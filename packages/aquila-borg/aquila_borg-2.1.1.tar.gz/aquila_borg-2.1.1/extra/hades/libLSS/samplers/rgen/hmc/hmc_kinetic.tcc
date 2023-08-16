HMCDensitySampler::HamiltonianType
HMCDensitySampler::computeHamiltonian_Kinetic() {
  CArrayType::ArrayType &momentum_array = *momentum_field->array;


  auto m_w = fwrap(momentum_array);
  auto r = std::real(m_w);
  auto i = std::imag(m_w);

  double Ekin = (r*r+i*i).sum() / (2.);
  comm->all_reduce_t(MPI_IN_PLACE, &Ekin, 1, MPI_SUM);
  return Ekin*0.5;
}
