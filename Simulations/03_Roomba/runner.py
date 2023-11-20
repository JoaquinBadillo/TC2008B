from model import CleaningModel
import argparse

# Function to execute the model multiple times using 2 to 10 agents and dump 
# results to an output file (used for pgfplots).

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run a bunch of simulations and output the results to a file'
    )

    parser.add_argument(
        'num_iterations',
        type=int,
        nargs='?',
        default=100,
        help='Number of iterations to run'
    )

    parser.add_argument(
        'width',
        type=int,
        nargs='?',
        default=25,
        help='Grid Width'
    )

    parser.add_argument(
        'height',
        type=int,
        nargs='?',
        default=25,
        help='Grid Height'
    )

    parser.add_argument(
        'display',
        type=bool,
        nargs='?',
        default=True,
        help='Show current number of agents'
    )

    parser.add_argument(
        'verbose',
        type=bool,
        nargs='?',
        default=False,
        help='Show iteration count and current number of agents'
    )

    args = parser.parse_args()

    f = open("output.txt", "w")
    f.write("num_agents dirt success_rate\n")

    for num_agents in range(2, 11):
        if args.display or args.verbose:
            print(f"Starting iterations using {num_agents} agents...")

        dirt_count = 0
        success_rate = 0

        for i in range(args.num_iterations):
            if args.verbose:
                print(f"Iteration {i + 1} / {args.num_iterations}")

            model = CleaningModel(
                num_agents=num_agents,
                dirt_density=0.1,
                obstacle_density=0.1,
                width=25,
                height=25,
                limit=500
            )
                            
            while model.running:
                model.step()
            
            dirt_count += model.dirt_count
            success_rate += 1 if model.dirt_count == 0 else 0
            
        dirt_count /= args.num_iterations
        success_rate /= args.num_iterations

        f.write(f"{num_agents} {dirt_count} {success_rate}\n")

        if args.display or args.silent:
            print(f"Finished iterations using {num_agents} agents.\n")
        

    f.close()