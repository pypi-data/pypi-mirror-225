using TensorFlow
using Distributions

sess = Session(Graph());

inputs = 3;

θ = placeholder(Float32, shape = [nothing, inputs])
m2lnL = placeholder(Float32, shape = [nothing])

layers = 2;
neurons_per_layer = 50;
α = 0.1;

function network(θ, layers, neurons_per_layer, α)
    x = θ
    weights = Array{Any}(layers + 1)
    biases = Array{Any}(layers + 1)
    for i=1:layers
        if i == 1
            weights[i] = get_variable("layer_" * string(i) * "_weights", [3, neurons_per_layer], Float32, initializer=Normal(0., sqrt(2./3.)))
            biases[i] = get_variable("layer_" * string(i) * "_biases", [neurons_per_layer], Float32)
        elseif i == layers
            weights[i] = get_variable("layer_" * string(i) * "_weights", [neurons_per_layer, 1], Float32, initializer=Normal(0., sqrt(2./neurons_per_layer)))
            biases[i] = get_variable("layer_" * string(i) * "_biases", [1], Float32)
        else
            weights[i] = get_variable("layer_" * string(i) * "_weights", [neurons_per_layer, neurons_per_layer], Float32, initializer=Normal(0., sqrt(2./neurons_per_layer)))
            biases[i] = get_variable("layer_" * string(i) * "_biases", [neurons_per_layer], Float32)
        end
        x = x * weights[i] + biases[i]
        x = max(α * x, x)
    end
    x = reshape(x, (-1))
    return x, weights, biases
end

output, weights, biases = network(θ, layers, neurons_per_layer, α)

loss = mean(0.5 * (output / m2lnL - 1)^2)

gradient = gradients(loss, θ);
weight_gradients = [gradients(loss, weights[i]) for i=1:layers];
bias_gradients = [gradients(loss, biases[i]) for i=1:layers];
