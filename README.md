# Kattis helper

- fetch the sample data for every problem
- run your solution against all `testcase.in` and `testcase.ans` files in a directory.

## Fetching data from a contest

`python3 fetcher.py -u https://ncpc19.kattis.com`

Will fetch all samples from the contest at the kattis-url, and for each problem `A` ... `N` place them in `data/A`, ... `data/N`.

Override the `data`-folder with `-o ${my_folder}`.
Use `-f` to wipe the `cache` and refetch.

If the contest has not started yet you can use `-w` to wait until a given time given on the format `HH:MM[:SS]`

At ncpc 2020 I plan to do the following:
`python3 fetcher.py -u https://ncpc20.kattis.com -w 11:00:05` to run my script 5 seconds after the contest has started, starting it in the background before the contest starts.


## Running your solution.

`python3 run.py -d data/A A.py` will run your progam `A.py` on all inputs in `data/A.py`. Similar to running `pypy3 A.py < data/A/1.in > data/A/1.out && diff data/A/1.out data/A/1.ans` for each input/output pair.

Use `-c` to specify a comman instead of a file.

`python3 run.py -d data/A -c './a.out'`
`python3 run.py -d data/A -c 'java A'`

Use the test cases to see what output `run.py` produces:

```
> python3 run.py -d test/H/ test/H.py
[AC] 0.11s test/H/1.in
[AC] 0.10s test/H/2.in
```

```
> python3 run.py -d test/H/ test/H_WA.py 
[WA] 0.12s test/H/1.in
[EXPECTED]:
2 28
---------
[GOT]:
28 28
---------
[WA] 0.11s test/H/2.in
[EXPECTED]:
1 30
---------
[GOT]:
30 30
```
