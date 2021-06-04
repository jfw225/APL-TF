from pipeline import Pipeline
from async_predict import AsyncPredict
from input_capture import InputCapture
import multiprocessing as mp
from collections import deque


def main():
    mp.set_start_method("spawn", force=True)

    ## The input capture (doesn't neccesarily need to be in the pipeline)
    q = deque(range(100))
    ic = InputCapture(q)

    ## Predictor
    predict = AsyncPredict(num_gpus=0, num_cpus=1)

    pl = ic >> predict >> Pipeline()

    results = list()
    while ic.is_working() or predict.is_working():
        if (result := pl.map(None)) != Pipeline.Empty:
            results.append(result)

    predict.cleanup()

    print(list(results))

if __name__ == '__main__':
    main()
