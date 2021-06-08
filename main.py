from pipeline import Pipeline
from async_work import AsyncWork
from input_capture import InputCapture
from testpipe import TestPipe1

import multiprocessing as mp
from collections import deque




def main():
    mp.set_start_method("spawn", force=True)

    ## The input capture (doesn't neccesarily need to be in the pipeline)
    q = deque(range(100))
    ic = InputCapture(q)

    ## Predictor
    predict = AsyncWork(num_gpus=0, num_cpus=5)

    ## Test Pipe
    tp = TestPipe1()

    pl = ic >> predict >> tp

    results = list()
    while ic.is_working() or predict.is_working():
        if (result := pl.map(None)) != Pipeline.Empty:
            results.append(result)

    predict.cleanup()

    print(list(results))

if __name__ == '__main__':
    main()
