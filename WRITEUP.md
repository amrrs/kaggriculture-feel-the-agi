# Kaggriculture: what we built, what we learned, what didn't work

Team "feel the agi". Final submissions: g012m and g010c04. Same agent, two different parameter settings. Code, harness and all the research notes are on GitHub (link below).

## The agent

It's one Python file. The first ten days follow a small library of recorded openings taken from public replays of strong agents, branching on which shops unlock on days 3 and 6, with a repair routine that kicks in when cash or tiles drift from the plan. From day 11 a reactive executor takes over. Every morning it re-plans the farm from what it can see: the shops, market inventory and prices, the rival's tiles and what the rival sold (you can recover that exactly from the inventory change), and its own cash and shed. It decides tiles and herd from a per-product market model, picks how many hands to hire by comparing the value of the routed work against the wage, and routes the workers with a small vehicle-routing local search. Market orders are simple on purpose: sell when produce reaches the shed, never hold for a better price, keep the shed under the 100-item cap, and put whatever product the rival is about to dump into slot 1 of the order list, because orders are processed slot by slot in lockstep.

The last thing we did was stop hand-tuning it. We ran CMA-ES over 25 of its behavioural settings, scoring each candidate against 123 recorded games of the current top-12 teams plus fresh games against our own earlier bots, then checked the winners on seeds and tapes the search had never seen. That found about +0.9k coins per game over our previous best, mostly from planting tomatoes earlier and selling premium goods earlier in the day.

## Where it landed

Offline, paired on untouched seeds, g012m beats our previous best 71% of the time and edges the top-12 tapes 68 wins to 64. Live, this family settles around 2650 to 2700. The top 10 was 2840 and up. So: a solid mid-table agent, not a prize one.

## What we learned, the hard way

Own income isn't the score. Our farms earn the same as the top three, roughly 105k to 115k coins. The games are decided in the shared market, and the top teams take about 10k more from us than they take from each other: tomatoes we never grew, so they sell 70 of them into an empty book, and premium goods that reach the market before ours. Rating only counts wins, so margin is irrelevant.

Selling is denial, holding is a gift. Every idea that held stock back, kept a reserve, or hired fewer hands made us a little richer and the rival a lot richer. Drip selling, price thresholds, dawn delivery loops, all negative.

The shops aren't as random as they look. At the end of each day the engine burns one random draw per empty tile on each farm before it picks the next shop, so one extra dig changes which shop opens. Steering it on purpose would need the hidden seed, which you can't infer in time. Worth knowing anyway; credit to leoprovorov for working that out in public.

The top three don't run a tape at all. From step one they play one integrated controller: herd sized from the first three shops, land bought on fixed days, tomatoes from day 8 in every world, 12 hands a day, no wheat churn, premium goods sold a unit or two after each shop tick. We extracted that playbook from their replays in detail. Bolting any piece of it onto a tape-plus-executor agent lost every single time, sometimes badly. It has to be built as one thing.

## What failed

Fourth quadrant (-4k). A tomato wave on our executor (-6k). The top-3 opening in front of our executor (-8k to -14k). A from-scratch reactive controller after one day of work (-30k). A transformer imitating top replays (falls apart after a few steps). Macro PPO self-play (about rank 55). Forecasting and racing the rival's sales. Copying the leaders' layouts. Evolutionary search over macro plans. Bigger search budgets for the router (it had already converged). And 46 of the 77 knobs we screened never change a single action.

## Things we'd reuse

Exact ledgers rebuilt from replays by re-running the engine's market rules. A "tape judge" that replays a top team's recorded game against your candidate on the same seed and shops. A fresh-seed bench that logs per-step time, because a slow step is a lost game. The CMA-ES harness. And pinning the shop sequence when comparing two builds, which cut the noise on paired margins by about 8x.

## Credits

Opening library from public replays. Early lineage from yhay81's Three-Day Shop Router (Apache-2.0). Executor base by Codex on our team. Order-book slot idea from thomastschinkel's The 2945 Farm. RNG analysis from leoprovorov. Most of the code and experiments were written with Claude and Codex as coding agents, with a lot of arguing in between. Apache-2.0.
