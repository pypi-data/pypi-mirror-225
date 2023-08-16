

static inline double get_u0(const double &u0, int epsilon) {
  return (1 - epsilon) / 2 + epsilon * u0;
  //  return (epsilon > 0) ? u0 : (1-u0);
}

static inline double ProductTerm0(double *u, double *u0, int *epsilon, int q) {
  double a = 1;

  for (unsigned int r = 0; r < 3; r++)
    a *= get_u0(u0[r], epsilon[r]);
  return a;
};

static double ProductTerm1(double *u, double *u0, int *epsilon, int q) {
  double a = 1;
  double G[3];

  for (unsigned int r = 0; r < 3; r++) {
    G[r] = get_u0(u0[r], epsilon[r]);
  }

  double F[3] = {G[1] * G[2], G[0] * G[2], G[0] * G[1]};

  return F[q] * u[q] * epsilon[q];
};

static inline double ProductTerm2(double *u, double *u0, int *epsilon, int q) {
  double a = 1;
  double G[3];

  for (unsigned int r = 0; r < 3; r++) {
    G[r] = get_u0(u0[r], epsilon[r]);
  }

  double F[3] = {
      epsilon[1] * epsilon[2] * u[1] * u[2],
      epsilon[0] * epsilon[2] * u[0] * u[2],
      epsilon[0] * epsilon[1] * u[0] * u[1]};

  return F[q] * G[q];
};

static inline double ProductTerm3(double *u, double *u0, int *epsilon, int q) {
  return epsilon[0] * epsilon[1] * epsilon[2] * u[0] * u[1] * u[2];
};
