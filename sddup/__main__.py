from sddup import SDDup
import sys

def main(args):
    try:
        experiment_type = "both"
        amount = 100
        if len(args) > 3:
            raise Exception()
        elif len(args) == 3:
            experiment_type = args[1]
            amount = int(args[2])
        elif len(args) == 2:
            experiment_type = args[1]

        sddup = SDDup()
        sddup.run_experiment(experiment_type= experiment_type, amount= amount)
    except:
        print("Usage: poetry run python3 sddup [experiment_type] [amount]")
        print()
        print("experiment_type - Type of experiment to be run, either 'pdf', 'xml' or 'both'. Default 'both'")
        print("amount - Amount of files to be generated and processed, must be a positive integer. Default 100")

if __name__ == "__main__":
    main(sys.argv)
