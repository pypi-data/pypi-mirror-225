inline double RandomNumber::gaussian_ratio()
{ 
    double u, v, x, y, Q;
    const double s = 0.449871;    /* Constants from Leva */
    const double t = -0.386595;
    const double a = 0.19600;
    const double b = 0.25472;
    const double r1 = 0.27597;
    const double r2 = 0.27846;

    do {    
        u = 1 - uniform();
        v = uniform() - 0.5;
        
        v *= 1.7156;
        
        x = u - s;
        y = std::abs(v) - t;
        Q = x * x + y * (a * y - b * x);
    }
    while (Q >= r1 && (Q > r2 || (v*v) > (-4*u*u*log(u)) ) );
    
    return v/u;   
}

