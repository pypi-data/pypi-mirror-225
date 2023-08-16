inline
HMCDensitySampler::HamiltonianType codeletHamiltonianPrior(int n0, int n1, int n2,
                               const IArrayType::ArrayType& adjust_array,
                               const ArrayType1d::ArrayType& pspec,
                               const IArrayType::ArrayType& key_array,
                               const CArrayType::ArrayType& s_array
                            )
{
    const CArrayType::ArrayType::element& e = s_array[n0][n1][n2];
    long powerPosition = key_array[n0][n1][n2];
    double Amplitude = pspec.data()[powerPosition];
    double adjust = adjust_array[n0][n1][n2];
    
    if (Amplitude == 0)
        return 0;
    
    double Eprior = adjust * (square(e.real()) + square(e.imag()))/Amplitude;

    if (isnan(Eprior)) { 
        error_helper<ErrorBadState>("NaN in hamiltonian"); 
    }
    
    return Eprior;
}

inline
HMCDensitySampler::HamiltonianType codeletGradientPrior(int n0, int n1, int n2,
                            const IArrayType::ArrayType& adjust_array,
                            double volume,
                            const ArrayType1d::ArrayType& pspec,
                            const IArrayType::ArrayType& key_array,
                            const CArrayType::ArrayType& s,
                            CArrayType::RefArrayType& grad_array    
                            )
{
    const CArrayType::ArrayType::element& e = s[n0][n1][n2];
    long powerPosition = key_array[n0][n1][n2];
    double Amplitude = pspec.data()[powerPosition] * volume;
    CArrayType::ArrayType::element& gradient = grad_array[n0][n1][n2];
    double adjust = adjust_array[n0][n1][n2];

    if (Amplitude == 0 || adjust == 0)
        gradient = 0;
    else
        gradient = adjust * e / Amplitude;
}


HMCDensitySampler::HamiltonianType HMCDensitySampler::computeHamiltonian_Prior(MarkovState& state, CArray& s_array)
{
    ArrayType1d::ArrayType& pspec = *state.get<ArrayType1d>("powerspectrum")->array;
    IArrayType::ArrayType& adjust_array = *state.get<IArrayType>("adjust_mode_multiplier")->array;
    IArrayType::ArrayType& key_array = *state.get<IArrayType>("k_keys")->array;
    
    double Eprior = 0;
    
    Eprior = codeletGeneralHamiltonian(adjust_array, 
                                       boost::bind(codeletHamiltonianPrior, _1, _2, _3, _4, boost::cref(pspec), boost::cref(key_array), boost::cref(s_array)));
    
    Eprior *= 0.5/volume;
    comm->all_reduce_t(MPI_IN_PLACE, &Eprior, 1, MPI_SUM);
    
    return Eprior;
}


void HMCDensitySampler::computeGradientPsi_Prior(MarkovState& state, CArray& s, CArrayRef& grad_array)
{
  IArrayType::ArrayType& adjust_array = *adjust_field->array;
  IArrayType::ArrayType& key_array = *state.get<IArrayType>("k_keys")->array;
  ArrayType1d::ArrayType& pspec = *state.get<ArrayType1d>("powerspectrum")->array;

  for (long n = 0 ; n < grad_array.num_elements(); n++)
    grad_array.data()[n] = 0;

  codeletGeneral(adjust_array,
                 boost::bind(&codeletGradientPrior, _1, _2, _3, _4, volume, boost::cref(pspec), boost::cref(key_array), boost::cref(s), boost::ref(grad_array)));
}
