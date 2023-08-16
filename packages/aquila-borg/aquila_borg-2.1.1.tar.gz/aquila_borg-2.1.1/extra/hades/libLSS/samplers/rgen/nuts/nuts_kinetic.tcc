inline
HMCDensitySampler::HamiltonianType codeletHamiltonianKinetic(int n0, int n1, int n2,
                               const IArrayType::ArrayType& adjust_array,
                               const ArrayType::ArrayType& sqM,
                               const CArrayType::ArrayType& momentum_array
                            )
{
    const CArrayType::ArrayType::element& e = momentum_array[n0][n1][n2];
    int adjust = adjust_array[n0][n1][n2];
    double Amplitude = (sqM[n0][n1][n2]);
    if (Amplitude == 0 || adjust == 0)
        return 0;
    
    double Ekin = (square(e.real()) + square(e.imag()))/Amplitude;
    if (isnan(Ekin)) { 
        error_helper<ErrorBadState>(format("NaN in kinetic hamiltonian n0=%d n1=%d n2=%d Mass=%lg") % n0 % n1 % n2 % Amplitude); 
    }
    
    return Ekin;
}

HMCDensitySampler::HamiltonianType HMCDensitySampler::computeHamiltonian_Kinetic()
{
    CArrayType::ArrayType& momentum_array = *momentum_field->array;
    ArrayType::ArrayType& sqrt_mass = *sqrt_mass_field->array;
    IArrayType::ArrayType& adjust_array = *adjust_field->array;

    double Ekin = codeletGeneralHamiltonian(adjust_array, 
            boost::bind(codeletHamiltonianKinetic, _1, _2, _3, _4, boost::cref(sqrt_mass), boost::cref(momentum_array)));

    Ekin *= 0.5;
    comm->all_reduce_t(MPI_IN_PLACE, &Ekin, 1, MPI_SUM);
    return Ekin;
}
