from matplotlib import pyplot as plt
import numpy as np

rng = np.random.default_rng(0)

def sbim_defectives(m, k, p, q1, q2):

    seeds = rng.choice([False, True], (1, m, k), p=[1 - p, p])
    network = np.copy(seeds)

    for community in range(m):
        for node in range(k):
            if seeds[0][community][node]:
                intra_mask = rng.choice([False, True], (1, k), p=[1 - q1, q1])
                network[0][community] = np.logical_or(network[0][community], intra_mask)
                for i in range(m):
                    if i != community:
                        inter_mask = rng.choice([False, True], (1, k), p=[1 - q2, q2])
                        network[0][i] = np.logical_or(network[0][i], inter_mask)

    return np.sum(np.ravel(network))

def average_defectives(trials, m, k, p, q1, q2):
    
    sum = 0

    for trial in range(trials):

        sum += sbim_defectives(m, k, p, q1, q2)

    return(sum / float(trials))

def main():

    x = np.arange(0, 0.011, 0.001)

    full = np.empty_like(x)
    inter = np.empty_like(x)
    intra = np.empty_like(x)
    seed = np.empty_like(x)

    trials = 500

    for i in range(len(x)):
        full[i] = average_defectives(trials, 20, 50, x[i], 0.1, 0.01)
        inter[i] = average_defectives(trials, 20, 50, x[i], 0, 0.01)
        intra[i] = average_defectives(trials, 20, 50, x[i], 0.1, 0)
        seed[i] = average_defectives(trials, 20, 50, x[i], 0, 0)

    plt.title("Simulated SBIM defectives")
    plt.plot(x, full, marker="x", label="Full infection model")
    plt.plot(x, inter, marker="x", label="Seed selection + inter-community")
    plt.plot(x, intra, marker="x", label="Seed selection + intra-community")
    plt.plot(x, seed, marker="x", label="Seed selection only")
    plt.legend(loc='upper left')
    plt.xlim([0, 0.01])
    plt.ylim([0, 160])
    plt.xlabel("Seed probability")
    plt.ylabel("Average number of defectives")
    plt.savefig("sbim_defectives.pdf")
    plt.clf()

if __name__ == "__main__":
    main()
