module convHMC
    using TensorFlow

    sess = 0; p = 0; δ = 0; g = 0; s = 0; n = 0; sel = 0; loss = 0; error = 0; ag = 0; output = 0;

    function isotropic_weights(params, C0, C1, C2)
        out_edge = stack([params[4], params[3], params[4]])
        out_face = stack([params[3], params[2], params[3]])
        inner = stack([params[2], params[1], params[2]])
        face = stack([out_edge, out_face, out_edge])
        middle = stack([out_face, inner, out_face])
        return reshape(stack([face, middle, face]), (C0, C1, C2, 1, 1))
    end

    function get_isotropic_weights(num_layers, kernel)
        w = Array{Any}(num_layers)
        b = Array{Any}(num_layers)
        for i = 1:num_layers
            w[i] = isotropic_weights(p[(i - 1) * 5 + 1: (i - 1) * 5 + 4], kernel[1], kernel[2], kernel[3])
            b[i] = p[i * 5]
        end
        return w, b
    end

    function get_3d_conv(num_layers, kernel)
        w = Array{Any}(num_layers)
        b = Array{Any}(num_layers)
        for i = 1:num_layers
            w[i] = reshape(p[(i - 1) * 28 + 1: (i - 1) * 28 + 27], (kernel[1], kernel[2], kernel[3], 1, 1))
            b[i] = p[i * 28]
        end
        return w, b
    end

    function convolutional_network(x, w, b, num_layers, N0, N1, N2)
        for i = 1:num_layers
            x = nn.relu(nn.conv3d(x, w[i], strides = [1, 1, 1, 1, 1], padding = "SAME") + b[i]) + x
        end
        x = nn.relu(x)
        return reshape(x, (N0, N1, N2))
    end

    function mse(x, g_, s_, n_, sel_, loss_params)
        N0 = loss_params[1]
        N1 = loss_params[2]
        N2 = loss_params[3]
        x = boolean_mask(reshape(x, N0 * N1 * N2), sel_)
        return reduce_sum(0.5 * (multiply(x, s_) - g_)^2. / multiply(n_,  s_) + 0.5 * log(n_))
    end

    function get_poisson_bias(_, __)
        return -99, -99
    end

    function no_network(x, _, __, ___, ____, _____, ______)
        return x
    end

    function poisson_bias(x, g_, s_, n_, sel_, loss_params)
        N0 = loss_params[1]
        N1 = loss_params[2]
        N2 = loss_params[3]
        x = boolean_mask(reshape(x, N0 * N1 * N2), sel_)
        return reduce_sum((g_ .- s_ .* ( .- p[1] .* x)).^2. / (s_ .* n_))
    end

    function setup(num_layers, N0, N1, N2, num_params, extras, loss_params, network, get_variables, Λ)
        global sess, p, δ, g, s, n, sel, output, loss, ag, error

        sess = Session();

        p = placeholder(Float64, shape = [num_params])
        δ = placeholder(Float64, shape = [N0, N1, N2])
        δ_ = reshape(δ, (1, N0, N1, N2, 1))
        sel = placeholder(Bool, shape = [N0, N1, N2])
        sel_ = reshape(sel, N0 * N1 * N2)
        g = placeholder(Float64, shape = [N0, N1, N2])
        g_ = boolean_mask(reshape(g, N0 * N1 * N2), sel_)
        s = placeholder(Float64, shape = [N0, N1, N2])
        s_ = boolean_mask(reshape(s, N0 * N1 * N2), sel_)
        n = placeholder(Float64, shape = [1])
        n_ = n[1]

        w, b = get_variables(num_layers, extras)
        output = network(δ_, w, b, num_layers, N0, N1, N2)
        loss = Λ(output, g_, s_, n_, sel_, loss_params)
        ag = gradients(loss, δ)
        #error = gradients(loss, p)
        run(sess, global_variables_initializer())
    end

    function evaluate(params, field, galaxy, selection, noise, mask)
        return run(sess, loss, Dict(p => params, δ => field, g => galaxy, s => selection, n => [noise], sel => mask))
    end

    function adjointGradient(params, field, galaxy, selection, noise, mask)
        return run(sess, ag, Dict(p => params, δ => field, g => galaxy, s => selection, n => [noise], sel => mask))
    end

    #function adjointNetworkGradient(params, field, galaxy, selection, noise, mask)
    #    gradient = run(sess, error, Dict(p => params, δ => field, g => galaxy, s => selection, n => [noise], sel => mask))
    #    params_gradient = gradient.values[gradient.indices]
    #    #println(params_gradient)
    #    #params_gradient = Array{Float64}(tot_num_conv * 5);
    #    #for i = 1:tot_num_conv
    #    #    for j = 1:4
    #    #        ind = find(x -> x == j, gradient[(i - 1) * 2 + 1].indices);
    #    #        params_gradient[(i - 1) * 5 + j] = sum(gradient[(i - 1) * 2 + 1].values[ind]);
    #    #    end
    #    #    params_gradient[i * 5] = gradient[i * 2];
    #    #end
    #    return params_gradient
    #end

    function get_field(params, field)
        return run(sess, output, Dict(p => params, δ => field));
    end
end
