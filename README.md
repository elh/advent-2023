# advent-2023 🎄

![AoC Stars](https://img.shields.io/badge/46-%F0%9F%8C%9F-yellow)

Refamiliarizing myself with Python. I completed [last year's in Clojure](https://github.com/elh/advent-2022).<br>
Inputs and answers are not checked in but can be provided in `inputs/` and `answers.json` respectively.

## Progress

`make` result:
```
Day 1:	＊ ＊ 	 [0.0011, 0.0072]
Day 2:	＊ ＊ 	 [0.0004, 0.0005]
Day 3:	＊ ＊ 	 [0.0049, 0.0025]
Day 4:	＊ ＊ 	 [0.0009, 0.001]
Day 5:	＊ ＊ 	 [0.0002, 0.0011]
Day 6:	＊ ＊ 	 [0.0, 0.0]
Day 7:	＊ ＊ 	 [0.0135, 0.0172]
Day 8:	＊ ＊ 	 [0.0024, 0.0142]
Day 9:	＊ ＊ 	 [0.0024, 0.0023]
Day 10:	＊ ＊ 	 [0.0105, 0.1087]
Day 11:	＊ ＊ 	 [0.0066, 0.0516]
Day 12:	＊ ＊ 	 [0.0171, 0.4218]
Day 13:	＊ ＊ 	 [0.001, 0.001]
Day 14:	＊ ＊ 	 [0.0009, 0.4406]
Day 15:	＊ ＊ 	 [0.0019, 0.0028]
Day 16:	＊ ＊ 	 [0.0081, 0.5986]
Day 17:	＊ ＊ 	 [0.6013, 2.3221]
Day 18:	＊ ＊ 	 [0.0399, 0.0015]
Day 19:	＊ ＊ 	 [0.001, 0.0038]
Day 20:	＊ ＊ 	 [0.018, 0.0714]
Day 21:	＊ ＊ 	 [0.0208, 0.4301]
Day 22:	＊ ＊ 	 [0.0454, 0.1833]
Day 23:	＊ ＊ 	 [0.016, 8.7534]
Day 24:	－ － 	 [None, None]
Day 25:	－ － 	 [None, None]

Results: 46 ＊, 0 Ｘ, 0 ?, 4 －, 0 s
Total time (s): 14.251
```

＊ = Correct, Ｘ = Incorrect, ? = No answer provided, － = Unimplemented, s = Skipped

## Usage

I have a nice harness that dynamically imports solution files and functions to run them. We can check all of them against saved answers to prevent regressions.

```bash
# Usage: python main.py <day> <part> <input_file>
# Example: python main.py 25 2 input.txt
#
# Expects files named `solutions/day<day>.py` with functions `part1` and `part2`
# that take the input as a string and return the answer. The file name <day> is
# 0-padded to 2 digits.
python main.py 2 2 input.txt

# Usage: python all.py [--skip <skip>]
#
# Runs all solutions in the stype of `main.py` and checks with answers present
# in `answers.json`. --skip is an optional csv of parts to skip. parts are
# represented as <day>.<part>, e.g. 1.1, 25.2
python all.py # also available as `make`. `SKIP=5.2 make` to skip specified parts

# Usage: plot_leaderboard.py [-h] leaderboard_file
# Example: python plot_leaderboard.py leaderboard.json
#
# Given a leaderboard json, prints out out a leaderboard point series in csv
# for your plotting convenience.
python python plot_leaderboard.py leaderboard.json
```

## Development

```bash
make lint       # mypy, ruff
make pretty     # black

make good       # runs lint, pretty
```

## Log (contains spoilers)

* 12/1
  * Wasn't sure if I would do it this year but I can't resist challenging friends to do it. Starting a private leaderboard with a bounty. I don't think I will have as much time as I did last year learning Clojure so opting for Python 🐍. Started on a flight to Taiwan for family 🇹🇼.
  * Day 1: Pleased with this idea of reversing the entire text and the words I am searching for to generalize the search.
  * Implemented a common main.py that can dynamically import solutions functions via importlib.
* 12/2
  * Played around with some Python tooling: ruff, black, mypy.
  * Added an all.py script.
* 12/3
  * Day 4: Clean single-pass iterative solution.
* 12/4
  * Day 5: Pleased with how fast I solved part 2 by coming up with a well bounded brute force solution. Performance is quite poor though taking 5s and I get a little confused thinking through the ranges. Done shortly after takeoff from Taiwan back to SF 🌉. UPDATE: performance improved by only considering boundary values.
* 12/5
  * Day 6: Heh... I solved it quickly with a janky binary search before looking up the quadratic equation.
* 12/6
  * Day 7: Finished 396th! This was the first night that I was at my computer at 9pm and prioritized speed so I'm quite pleased with this. My approach treating hands as a dict of card -> count was amenable to handling jokers 🃏.
* 12/7
  * Day 8: I was surprised that this math was needed as early as day 8 so I waited for my naive solution to complete a little too long.
  * At this point heading into travel next week 🇬🇧🇮🇳, I am leading 11 coworkers in my private leaderboard. I'm having a ton of fun chatting with the non-engineers doing it for the first time - 2 of them occupying 2nd and 3rd place.
* 12/9
  * Day 9: Done before bed in London after a 10 hour flight next to toddlers and 14K steps around xmas markets 🎅...
* 12/10
  * Day 10: Part 2 is the first puzzle to defeat me on the initial sitting at 6am jet lagged in the citizenM Bankside lobby. I'm familiar with winding numbers but have difficulty adapting the idea to the ascii grid after horribly fumbling the set up in Part 1.
* 12/11
  * Day 11: Part 1 completed in a taxi on the way to Heathrow airport.
  * Day 10: Part 2 revisited and solved using the even-odd rule for winding numbers and checking on cardinal directions from a given point. Great puzzle! We handle corners by treating them as connecting on one side. The next seen corner either connects on the opposite side completing the wall or on the same side which cancels it out. Some fun corner cases like handling "S" and handling unconnected pipes are done as preprocessing. Done before falling asleep the flight from London to Delhi on the way to a coworker's wedding.
* 12/16
  * Wrapped up an incredible wedding in Jaipur 🎊!
  * Day 12: Part 2 solved with DP by treating `s[1:]` as the subproblem and using the `@cache` decorator.
  * Quickly got through Days 13-16 part 1's so I have access to part 2's for the flight back in case I'm not too sleepy 😪.
  * Day 14: Part 2 solved by detecting loops and finding equivalent positions via modulo.
  * Day 16: Performance improved reusing previous results. `cast_light` returns a graph of lights and downstream lights which we can optionally take as an argument as well and build upon.
* 12/17
  * Day 18: Part 1 solved actually materializing the grid and doing a flood fill from the exterior of a bounded zone. Part 2 kicked my jet lagged butt. I realized somewhat quickly that I could treat the grid as an integration of scanline slices which only requires me to keep track of boundaries and then sum up the incremental areas. Debugging off-by-one errors due to the grid and other geometry corner cases was a pain without good visualization tools and the real inputs being very large. UPDATE: TIL of Pick’s theorem...
* 12/18
  * Day 19: Part 2 solved by working backwards: identify each assignment to "A" and with a range of possible values, tighten it going backwards through the condition graph.
  * Day 17: I got tripped up figuring out how to encode "number of steps in current direction" into the graph state for Dijkstra's. I encode the current location, the previous direction I came from, and the number of steps in that direction. Slowest part 2 so far.
* 12/19
  * Day 20: Part 2 solved by learning a lesson from previous days and investing in visualization tools early. I was quite surprised to find that my input graphs were highly isolated and this turned into another LCM of cycle lengths. Because I could imagine graphs that were far more entangled (like hash functions) and we had a similar puzzle this year, I didn't expect this approach to be applicable.
* 12/20
  * Day 21: Oh man. I was really excited because I had a lot of ideas for Part 2 quite early when the first people were starting to complete it but made one big oversight: adjacent grids would alternate parity of starting step. Ended up giving up for the night. I had seen that each grid would enter a tick-tocking steady state and that the input was specifically designed to be conducive to diamonds. Thought this also required some input-specific observations like the last puzzle but was much more interesting.
* 12/21
  * Day 22: This was fun to implement. A brick blocks another if its x and y ranges overlap and its max z is 1 less than the other's min z. Drop all of the blocks and keep a track of what blocked it. Calculating the chain reaction is then as easy as part 1 just traversing the dependency graph.
* 12/22
  * Day 21: Part 2 solved by generalizing how square diamonds tile over the given square grids. After getting some graph paper and making a utility script to quickly visualize the filled graphs, it was pretty quick to derive a pattern for the shapes that emerged (day21_notes.txt). Verification of computed results for step sizes built confidence in the solution. Taking a step back, I think this is a pretty fun one.
  * Day 23: Pre-processed the maze into a graph of "branch point" nodes and distances between them. Then, just naively did an exhaustive traversal of all permutations like in part 1. Runtimes are starting to get quite slow but I can't be bothered to optimize at this point 🙃🎄.
* 12/23
  * ^ Can't help it. Fidgeted with perf and bring total runtime down 66%.
* 12/24
  * Add utility for plotting a leaderboard. Turn AoC's JSON format into a timeseries CSV.
