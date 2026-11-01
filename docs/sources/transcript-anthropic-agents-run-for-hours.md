Source: "How to Build Agents That Run for Hours (Without Losing the Plot)", Ash and Andrew, Anthropic Applied AI, AI Engineer conference. Transcript pasted into the chat by Boroon on 25 October 2026, from https://ai.engineer/talks/mR-WAvEPRwE#edited-transcript. Saved verbatim as pasted.

---

Transcript:

0:15

Um, I'm Ash. Uh, this is Andrew. We both work in, uh, as engineers in our Applied AI, uh, team here at Anthropic. Um, and the kind of topic for this session was, uh, inspired by a blog post we put out, uh, just a couple weeks ago actually, um, about how to think about building, uh, agents that can
0:35

actually run for really long extended periods of time. You know, we're talking five, six-hour-plus kinda runs. Uh, I think we've all seen these kind of demos, you know, of like companies being like, "Hey, we've like one-shotted a browser," for example, but not necessarily sharing like some of the details into what goes into the harness, and that's what
0:54

we kind of wanna talk about today. So the first half, um, my amazing colleague Andrew will talk about, a little bit about basically how we've got here some of the primitives that we've shipped in Claude Code, um, and you know, where we are today.
1:09

Um, and then I'll hop back on stage to talk a little bit about, um, some of the more experimental stuff that we're playing with, the harnesses, um, as well as, you know, a few examples of, of what we've seen.
1:20

But over to you.
1:21

Sounds good. Thank you, Ash. And yeah, thanks everyone for joining our first session of the AI Engineer Conference, so glad you're spending it with us. Uh, my name's Andrew.
1:31

I'm on the Applied AI team based out of London, working as a solution architect with a lot of our digital native and industries customers. So, um, yeah, I'm gonna give a little bit of a history tour, a trip down memory lane, but really with the focus on all the things that we've shipped that lead to agents being
1:47

able to run, uh, for multiple hours or even days at a time. Um, and then I'll hand over to Ash to do more of the, the state of the art.
1:54

Right. Okay. So, um, a little quote from or on Twitter from Boris, the creator of Claude Code. This was on the one-year anniversary of Claude Code. Uh, basically saying a year ago, Claude was struggling just to write bash commands and escaping strings.
2:09

Um, and it could run for, you know, maybe 20 minutes at a time. And then we're now at the point where almost all of Claude Code is being written by Claude Code, and it can run effectively for days at a time.
2:20

Uh, so sort of a, a big, a big swing over just the course of a year, and I'll walk through that history, uh, a little bit now. But just to-- Maybe I'll zoom in here.
2:31

Um, just to sort of frame the problem up, like why, why is it that it's really difficult for these agents to run for extended periods of time? Um, I think broadly there's three big buckets.
2:42

Uh, some are more intuitive than others. So firstly, context. I think we all understand context window is very much finite, so you start a new session, there's like amnesia.
2:50

The agent has to start from scratch, so you need some sort of memory component. Um, also, as you're working through a context window, there's this notion of context rot.
2:58

So, uh, there's less coherence as you're, you're getting deeper into that session. Uh, also, you might get to the point where, uh, the model actually exhibits what's called context ans-anxiety.
3:09

So it gets kind of nervous as it reaches the end of its context window, and it just quickly hurries up to finish what it's doing. Um, this kind of leads into planning.
3:17

So, uh, in general, models are not that great at planning just out of the box. Uh, they might try and do everything in just one shot, or for example, they might build half a feature and then stop, or they might just run out of context altogether and sort of leave a half-finished, uh, app built.
3:34

Um, but then maybe less intuitively, um, models are really bad at judging their own output. So I know we all know that models can be sycophantic and sort of tell you what you want to hear, but this applies as well to, to coding tasks.
3:46

So it might look at a feature and see that it's sort of half, half-baked or a little bit implemented and say, "Yeah, okay, uh, that looks done," and then it'll move on to the next thing.
3:55

Or it might build a feature like a button, but actually the back end, you know, it doesn't exist for it. There's sort of no-- nothing behind that, but it looks like the feature is done.
4:04

So, um, I know Ash will talk quite extensively of so-some of the new techniques we have to, to help with this, um, specifically, so models can become better at judging their own output.
4:14

So there's, there's two ways really we can, we can fix these things. Uh, the first one is obviously the model. So, um, baking it all into the model weights themselves.
4:24

And I'm sure you've all seen this, this METR chart. It's basically how long can an agent run for with a minimal scaffold, uh, where it's completing 50% of the tasks.
4:34

And you'll see from Sonnet 3.7, it's around one hour, and up to Opus 4.6, one year later, it's at 12 hours, so an entire day. Um, and we've of course, you know, managed to get that running much longer.
4:46

Other people have as well, but this is just a sort of very minimal scaffold.
4:51

The second thing that you can do is, of course, make changes to the harness itself. So this is the scaffolding, um, around the model. And we have the Agent SDK, which ships with all the primitives that we've been building over time.
5:05

So there's the core agent loop itself, where you have Claude model that's determining what to do, what tools to run. Uh, maybe it's pulling in some tools from MCP servers.
5:15

Uh, it might delegate some tasks to a sub-agent. It's bringing in all the context from things like CLAUDE.md or the skills that are loaded or slash commands. Uh, there's a whole permission system.
5:25

And th-this, this will change over time as well as the models get better and improve. But these are sort of the, the core primitives that we're working with. And then, of course, you use this framework to, to build your own harness for whatever it is you're trying to do, such as some of the things that Ash will
5:39

show, uh, later on when we get into more long-running agents. Uh, I think what's also interesting is just looking back at the last year of releases is that when we've released a model, we've always also released a lot of harness changes alongside the models.
5:54

So really these things are co- co-evolving together. So we'll just look back, um, I suppose firstly just pre-history, um, beyond, you know, one year ago. I think we all remember that, that period where Claude had the artifact section of claude.ai and, and, uh, Sonnet 3.5 was the first model that really showed promise when it came to coding,
6:14

and it can now verify that. It could look at what it had built and sort of iterate from there, and that was quite an aha moment, sort of pre-Claude Code.
6:22

Uh, but then also we shipped computer use, so it could start clicking around, taking screenshots, um, testing its own code, as well as MCP spec, uh, which enabled it to sort of use tools.
6:34

So then getting into Claude Code. Uh, this is February 2025. So this is about just over a year ago. Um, Sonnet 3.7 was released and this was sort of state-of-the-art on SWE-bench, and Claude Code was released in research preview.
6:47

And I think an, an interesting quote that I pulled from this release actually is that the goal of Claude Code was to better understand how developers use Claude for coding to inform future model improvements.
6:59

So essentially when we released Claude Code, the whole idea was for it to be somewhat experimental to inform how we actually improve the base model itself. And you'll see this trend that over time the models become better, uh, the harness, certain aspects of it might become less necessary or it will evolve.
7:16

Um, just, just in terms of, uh, these slides as well, in the bottom left corner, these are some of the things that are, are sort of the focus of these releases, whether it's, uh, context or planning, uh, or verification, and then some, some stats.
7:29

But I'm not gonna sort of read everything. Um, so yeah, next, this was around May time of last year. Opus 4 and Sonnet 4, 4 were released. And just in general, um, these tools got much better at sort of managing their own context and getting to task completion, uh, without reward hacking or anything like that.
7:46

And then, uh, Claude Code became GA as well, and we released the Claude Code SDK. So sort of the, the harness powering Claude Code.

7:55

Um, a little interlude here from the timeline. I think everybody now knows about this Ralph Wiggum technique. Uh, you might not know that it was actually last July that this was-- that this came out, uh, when, when Geoffrey Huntley initially released the paper because it really sort of gained a lot of traction around, say, December or so
8:13

of last year, uh, when, for example, people started playing around with it themselves. Claude also released our own, uh, Ralph loop within the, the Claude Code, uh, harness itself.
8:23

But essentially it's, it's quite sort of a simple technique that you're just taking a prompt and you're feeding it into Claude Code CLI, for example, and then you're just running that on a loop until, uh, all the tasks are complete.
8:36

It's a little bit deeper than that. I, I think people tend to simplify it. There's actually a few phases where it first, you know, would have some kind of planning where it breaks down that prompt into a few different features, and then it would pick sort of one task from that and start a new session and then
8:51

work with a fresh context window. So a lot of those concepts were, were applied in the Ralph loop, but I think, um, why it caught so much attention is because it sort of seemed really simplistic.
9:01

And he put it, uh, deterministically bad in an undeterministic world. So the idea being that it's better to fail predictably than it is to succeed unpredictably. Um, when we actually created our own plugin for this in Claude Code, you'll see-- Well, I don't know if people can recognize what, what the major difference is.
9:20

There's some people say, you know, that's not a real Ralph loop. Um, the idea is that this is just running within a single Claude Code session, so it's not creating a fresh context window.
9:29

It's just relying on compaction to happen over time. So, you know, maybe it's not considered sort of a real Ralph loop, but you'd set the max iterations, you'd set a, a s- a safe word, and then essentially a stop hook would intercept, uh, when Claude would typically stop.
9:43

And if it's not finished, it would just sort of continue until it hits one of those, uh, exit criteria. Okay. So onto, uh, Sonnet 4.5. This was when the model just generally started getting better again at, at handling its own context.
9:59

So this is when it became more context-aware, tracking how many tokens had been consumed. So as it got towards the end of the context window, it sort of understand that and it could manage its own context.
10:10

Um, Claude Code 2.0 also shipped. This is where we introduced checkpoints, so actually keeping track of, of the code over time, being able to rewind to previous parts of the session.
10:22

And then we released-- We just sort of renamed the Claude Code SDK to the Agent SDK, and that's because we realized it's much more general purpose than actually just for coding.
10:31

So you'll see we're talking about coding a lot right now, but I think what's very interesting is applying these long-running harnesses to, um, other domains as well.
10:41

Uh, at this point, we could run for about thirty hours or so, uh, with Claude, uh, Sonnet 4.5. But then completing the family with Haiku 4.5 and Opus 4.5, this is where it got really interesting because all of a sudden running many sub-agents became really economical, and Opus 4.5 became really good at planning.
11:03

So we could start doing things like using Opu- Opus 4.5 for planning, um, and then using Sonnet 4.5 as the workhorse for really executing all of that code. Um, and then there's, there's a big, uh, couple months as well because this is when we released Skills, which again, very good at, uh, making use-- effective use of the
11:20

context with this notion of progressive disclosure. So just the front matter of the skill is loaded in instead of sort of all of your tool descriptions, you know, which can consume quite a lot of the context window up front.
11:32

Um, and then sort of the entire rest of the body of the skill is loaded in if it's instantiated, followed by, say, some references, um, to even, even code that could run more deterministically.
11:43

And then more context improvements, things like programmatic tool calling. So instead of running a bunch of tools, pulling all of that into, to context and then trying to process it, actually just writing code on the fly and being able to sort of run a series of tool calls and then just get the final result back.
11:59

And again, this is all just to improve the, the usage of, of the context window.
12:05

Okay, so t- a lot going on on this slide. But at this point, um, this is around November time, we released our first blog post on long-running agents and, and how you would go about building these.
12:16

So a lot of the concepts I've already described, um, should make this fairly easy to understand actually, where, say, a human would write something like, you know, write me a browser or create a Slack clone or a Salesforce clone, just something like really, really vague.
12:31

And, uh, the first thing that would happen, um, in this harness that we built is there's an initializer agent that would take that simple prompt, and it would break it down into a series of, of persistent artifacts.
12:44

The first being a feature list of, say, X number of features. feature_list.json because we actually found the models [chuckles] might overwrite markdown files, whereas they're, they're less likely to just overwrite JSON files, which is kind of interesting.
12:58

Um, it would also write a progress file. Um, of course, sort of start the Git repo, uh, build an init script, and then just have a flag for, you know, whether the features are complete or not, if they sort of pass all the tests.
13:11

Um, from there, it would go into this harness loop where, uh, there's multiple different steps here. So the first one is, you know, again, in a fresh context window, just getting the bearings.
13:22

What's the present working directory? Um, what's the, the progress file say? Okay, and then, um, doing a smoke test or running the init script, so it didn't have to figure out how to do that every time, get the server up and running, et cetera.
13:34

Uh, and then picking one feature, only one feature that, that hasn't passed all the tests. Um, implementing that feature, doing some actual tests, much so-- verification loop, much like a human would do using Puppeteer in this case.
13:48

Um, and then if, if everything passes, actually writing the Git commit and, um, changing the, the state of, of this particular feature to passes. And then if there are any features that are unfinished, just continuing that loop in a fresh context window.
14:03

So we're starting to layer in a lot of these concepts here, fresh context windows, these sort of persistent artifacts, verification loops, um, really good planning up front. You'll see like this, this is sort of the first iteration of, of these long-running harnesses here.
14:20

Okay. So, uh, continuing with the history tour. So then Opus 4.6, Sonnet 4.6. Um, these models were really great because Sonnet 4.6 was basically offering that Opus-level intelligence more at the, the Sonnet price, and it became again, like very much a workhorse for a lot of Claude Code.
14:37

Um, and Opus 4.6 just became really good at planning. We, we called it like very much an agentic model. So Opus 4.6 was great at, at deciding like which tools to use and just being able to run for much longer.
14:51

Uh, if you recall that METR chart, you'll see that this was a jump from about four hours up to twelve hours with sort of that very simple harness. So this model is like very, very agentic.
15:01

And then along with that, um, with some of the research we had done, we released agent teams, which the idea being in Claude Code, this sort of more general-purpose way for you to, say, scaffold out your own set, set of, of custom agents.
15:14

And the innovation with agent teams is that instead of everything reporting back into the main agent, um, the actual sub-agents could, could communicate with each other. So they sort of had their own way to coordinate and then report back to the main agent only when it was required.
15:30

Um, we also introduced server-side compaction, which basically meaning that these models can now just run indefinitely, and compaction could just sort of, you know, happen on the server side.
15:40

And then, um, this one million context GA. So now we have like one big context window. You see like the models are getting better. Maybe you can just run a lot, you know, within a single context window even instead of necessarily needing new sessions all the time.
15:53

You see how things start shifting over time. So that's sort of the, uh, the whole overview. You can see all of the different, uh, releases that I shared here on this table, and you can see how it's changed from, say, Sonnet 3.7 at one hour, uh, to twelve hours with Opus 4.6.
16:11

And then we have our own anecdotes as well, um, where tasks would take, say, you know, like twenty minutes when it was Opus 3.5, and now we're building, say, fully fledged apps that don't have to run for, you know, thirty hours.
16:25

They can run-- typically, we're seeing like, say, three to five hours, you can build like a really, really fully featured application that, that runs out of the box.
16:35

So what's really interesting is, is the harness doesn't just disappear as the models get better. It's really evolving as the models change over time. And it's really fascinating to sort of find the, the gaps in the model and then fill that in with the harness.
16:51

And then you train the model on, um, the-- using that aspect of the harness. Then maybe at some point you actually remove that entirely and sort of this iterative, uh, loop just keeps happening over time with, with more and more of these sort of co-releases that we have.
17:04

So, um, yeah, hopefully that was an interesting little trip, uh, back through the Claude evolution, uh, and how it applies to the long-running agents. And so I'll, I'll hand over to, to Ash to continue with where we are today, uh, in terms of the state of the art. [audience applauding]
17:28

Ugh. All right. Um, quick question. Any of you guys have any agents running at the moment in the background doing work while you're here? Just one, two, three? Okay.
17:41

Probably should be more of you. Um, uh, hopefully by the end of this you'll have some ideas to like take away and actually like put into practice. Um,
17:50

so yeah, that's, that's the history. Um, and I quite like that quote that, uh, Andrew talked about where the frontier doesn't really shrink, it just, uh, moves. And so what I wanted to talk about a little bit is some very simple, uh- Kind of harness patterns that we've been playing around with internally that we use to, to
18:11

build these, like, very fancy one-shot demo apps. Um, but also, you know, we're experimenting with this stuff in post-training, um, in, in RL. How do we make our models and, and just their general behaviors more adept at, uh, autonomous work?
18:27

So if you've ever tried to get, um, an agent to try and review its own PR, um, you'll kind of understand, uh, where this is going. So
18:42

this general, uh, idea is shamelessly kind of stolen from, from GANs, uh, generative, uh, kind of adversarial networks. So you have this, uh, generator kinda model, and then you have some sort of discriminator, um, and, uh, you have some sort of adversarial pressure between them.
19:01

You know, the generator builds, the evaluator grades, um, and the whole idea here is we're splitting up, you know, the context windows, uh, system prompts, uh, uh, the jobs entirely, right?
19:14

The evaluator here isn't just reading diffs, but it's actually using Playwright, um, to open live pages, click around, try things out, um, and then it eventually hands back whatever critique it's decided back to the actual generator, and you, you know, you kinda continue that loop.
19:31

Contrast that with what most people today are doing, which is kind of using one Claude Code session, telling it to check its own work, um, uh, and kinda loop that way.
19:40

So the obvious question for me at least is, you know, if the evaluator is also just an LLM, um, why doesn't it just rubber-stamp it too?
19:50

And so the key idea that we're kind of exploiting here is, um, yes, the evaluator is still, uh, a large language model, and yes, it's still going to be biased towards, uh, liking large language model-style outputs.
20:05

Um, but tuning a standalone critic, um, to be harsh is actually very tractable, but tuning a builder to be somewhat self-critical, um, is, is not. I think a really good analogy for this, right, is, is same as humans.
20:19

Um, it's very easy for, uh, me to, you know, critique, uh, uh, a lovely piece of artwork or, you know, a fine meal. Um, much harder for me to actually go ahead and like, you know, paint that, uh, or, or cook that meal myself.
20:34

So what we're doing here is exploiting the gap between the ability of an LLM to be kind of a, a critic, uh, versus a, a generator.
20:42

So the next thing I kinda wanna talk about is like how do you actually think about designing, uh, these critics? It's very similar to the process of creating good evals.
20:51

But in the context of full-stack apps, there are a lot of fuzzy kind of areas which go into what makes something good. It's not just does it work, but does it look good?
21:01

Does it feel good? Um, is there an element of taste, um, uh, in these kind of products as well?
21:08

So this is where we've been doing a lot of experimental work, um, especially when trying to, you know, imbue Claude with design taste and post-training, um, but also, um, you know, create these kind of front-end design skills that we kinda put out there and just generally improve the, the front-end design, uh, ability of, of our models.
21:27

So the way we think about this is
21:31

most people say you can't grade taste, but, you know, we think you can if you have a, a strong enough opinion on it, and you just kind of write it down.
21:40

And so the way we do this at least is with kind of creating a rubric with four criteria: uh, design, originality, craft, and functionality. Um, we actually weight this towards, uh, design and originality.
21:54

Um, we've kinda shifted the weightings between these four things, uh, depending on which model's in play. But at the moment, you know, Opus 4.6 is pretty good at, at, at functionality already.
22:04

So the problem that we're trying to overcome is how do we prevent things like, you know, purple gradients, general kind of AI slop-type aesthetics in general? And we kind of just go ahead and calibrate this with a few short examples, um, on reference sites, so the evaluator's kind of taste converges on our own.
22:23

Um, and let me show you an example, I guess, of what this actually looks like, uh, kind of in, in practice. So
22:32

this is just an example, um, of a model, uh, going through this similar kind of loop. Generator, uh, evaluator launches Playwright, navigates, screenshots, scores on those kind of four criteria, w- writes critique, and then hands back to generator.
22:49

So all of these examples are just HTML and CSS only. Um, they've gone through for maybe four hours, five to 15 rounds. Um, I think the interesting thing here, um, which is quite unique and something which you wouldn't necessarily get, um, if you're just using a single kind of agent loop, is that the thing pivots, right?
23:08

So imagine the generator gets stuck on one of the four criteria. Let's say it's like really struggling and constantly scoring low on originality. Um, you know, uh, this kind of GAN-style harness which we're using will just throw the whole thing out and try again from scratch.
23:24

Um, whereas, uh, in a single pass generation or a Ralph loop, um, it gets... it keeps trying to patch the same thing. Uh, and this kind of ability to kind of course-correct over very long, uh, kind of time horizons is something which is quite unique, uh, to kind of breaking down, uh, the different roles, uh, that go
23:42

into, to building something. So that was just an insight into, I guess, how we think about the front-end component. Um, but how to go from kind of like just nice pages to fully working apps, we added, uh, one more role, um, a planner.
23:59

And so again, sounds very simple. Um, it's ultimately just taking kind of a one-line prompt, um, and then breaking it down into, uh, a very deliberately high-level, uh, kind of spec.
24:12

So what it does is actually just spec the granular, um, uh-- Sorry, it kinda specs,
24:20

uh, the general workflow into a series of sprints. Um, what it doesn't do and, and what most harnesses do today is necessarily try and plan the granular technical details of, of the product.
24:32

The reason being is, you know, one, it's very likely to still make an error, but when it does make an error, it's going to cascade, um, through every single one of these sprints, uh, and kind of magnify errors over a multi- multi-hour time horizon.
24:46

If you kinda squint, uh, at this, um, this is kind of just, you know, a very simple kind of like PM, uh, IC, and, and QA kind of org structure, right?
24:56

Like, we didn't invent this, um, we just kinda gave each role its own kind of context window. Um, and the bit which is kind of interesting, I think, to talk about is the glue between the generator and the evaluator in this kinda setup.
25:12

So before the generator actually goes ahead and writes a single line, um, we have the two agents basically negotiate what done actually means. And so let's say the generator proposes, um, "I'm gonna build X feature, um, and you should verify it by testing Y."
25:33

Um, the evaluator might push back and be like, "Actually, uh, the scope is too big, and those tests that you propose are a bit too weak, uh, and you've missed XYZ edge case."
25:42

And you basically have this back and forth, uh, via files on disk. One writes the markdown, um, the other reads it, um, and you iterate until both agree. And then once you kind of reach that kind of condition, um,
25:56

then you actually start building. Uh, and then the evaluator kinda grades against the contract, um, that those two agents have decided between themselves, not the original spec, which the planner has kind of one-shotted at the beginning.
26:10

And why this matters, um, as it kind of bridges this kind of idea of kind of user stories, uh, i.e. the spec, um, and kinda converts it into slightly more tangible, testable kind of assertions, some sort of contract, uh, without the planner having to overspecify kind of upfront.
26:30

And I think this is kind of the key innovation that the Ralph loop never really had. It had a kind of fixed plan.md style, uh, kinda thing, but nobody, uh, on the other side is necessarily arguing with kind of the main loop.
26:46

And again, it comes back to, like, having these separate context windows and adversarial pressure. So let me show you an example of, uh, a very simple prompt that we had, um, uh, in a solo kind of loop versus, uh, the harness that we just discussed.
27:03

So the prompt was basically, "Build a retro game maker," um, and, and that was it.
27:10

And I'm not, you know, gonna, gonna try and convince you that this is, like, necessarily the most cost-effective or most efficient way to try and build an app. Um, as you can see, one, it takes, uh, at the moment, an extremely long amount of time.
27:24

Um, two, it's very expensive. But also, uh, as we'll see in a second, a lot of the stuff actually starts working only, uh, with this harness, um, when it didn't in a kind of a solo loop.
27:36

So this is, uh, what it kinda looked like, the opening screen, at least when we didn't have the harness. Um, pretty simplistic, a little bit boring, um, but it still looks nice, right?
27:48

Um, if this were the whole app, uh, you'd ship it, but it's kind of the bait, I guess, uh, if you will. Um, this was kind of the, uh, sprite editor, if you will.
27:59

Again, it still looks fine. Um, the canvas is there, the palette, the frame timeline, live preview. Maybe it's a little bit cramped, um, uh, and the color picker is just black swatches, but it, it kinda works.
28:11

Um, clearly, the agent, like, actually did understand what it was trying to do. Um, and then the one thing that you ha- actually has to do, um, uh, which is play mode.
28:22

Entities rendered, um, score, health, all the other things which go into an actual game. Pressing an arrow key does nothing. Pressing a space key did nothing. Um, the agent really didn't have any idea, um, how to test itself, uh, uh, what it actually meant to play a game and, and actually succeed.
28:42

Um, and yeah, this is kind of the same prompt, same model, um, and this is kind of the, the breaking point. It, it kind of looks done on the surface, but when you try and actually push it to its limits, it just, uh, it just kinda failed.
28:56

And then if we ran the same prompt with the same model, this is kind of what it looked like, uh, when we ran the harness. So this was about, yeah, two hundred bucks, six hours.
29:05

Um, [laughs] first up, it decided to name itself, um, Retro Forge. Um, it decided to, like, create a, a new project dialogue, um, have a very nice canvas. Um, none of that was in our prompt.
29:18

So this was all the planner, um, deciding like, "Okay, uh, here's what the product decisions should look like," and then, you know, the two other agents deciding, "Right, how am I gonna test this?"
29:30

Um, if we look at the sprite editor, um, we have kind of a full fifty-four color palette, um, the kind of eight-bit preset from the project dialogue flowing through.
29:41

Um, you see the sprite at actual game scale. Um,
29:47

it's a lot more complete, uh, as a product in general. Um, we had a whole new kind of AI-level assistant. This is where it kind of started to get recursive.
29:59

The planner had decided like, "Right, we should have some AI features," um, uh, which is just a very vague line in the spec. And the harness turned that into a full AI-level assistant inside the app that it, it was building.
30:10

So, you know, someone could come in and say, "Hey, create a castle, uh, with sprites guide-- gu-guarding it," let's say. Um-
30:19

This is something which a solo run would never even attempted to look at. Um, without the planner, that phrase just becomes, never even comes, becomes like a work item to look at.
30:30

Then finally, I guess, um, uh, the actual results kind of applied. So
30:37

play modes, um, you know, you had this whole debug HUD in the top left, um, which you can clearly tell is to make life easier for the, for the, for the evaluator, for example.
30:47

Those numbers are live. The physics loop is actually running. Um, arrow keys work, the player moves, um, collides with castle walls. Um, because the evaluator actually launched the game, tried to play it, knew necessarily like what, what features needed to be tested to make this game kind of real and successful.
31:08

Um, and the difference between this output and, you know, the previous output is entirely just scaffolding. And it's a very simple loop ultimately, but the results are quite startlingly different, at least.
31:19

And so in case you're curious, the kind of things which the evaluator did catch, um, are pretty basic kind of stuff. It's things like, um, you know, FastAPI route ordering, um, passes every unit test, but might actually break in prod.
31:38

The evaluator, um, catching things like the delete key, um, having some kind of Boolean logic bug. Um, again, these are things which were only caught because the evaluator's actually using the app.
31:49

Um, it's things which might get through CI in a Ralph loop, um, um, but this isn't, you know, that level of specificity isn't something which happened by accident. And so [chuckles]
32:04

this is the kind of level of detail which these models are kind of going to at this point in time. So we talked about the kind of contracts that the generator and the evaluator would write between themselves.
32:14

For this app, um, it decided that there were 27 contract criteria. That's the level of granularity which we found, you know, that you really need to make findings kind of actionable.
32:24

If you have vague criteria, you have vague critiques. The generator just kind of shrugs and does things. Whereas if you have granular criteria, um, the agent knows, okay, I need to fix this exact line.
32:40

What's kind of interesting, I thought, you know, uh, and I want to be honest about this part, is that out the box, Claude is a really, really bad just general QA agent.
32:49

Um, Andrew talked about this, uh, a little bit, uh, in his bit, right? But the same kind of sycophancy and generosity bias that everyone hits with, uh, general LLM as a judge systems also applies here.
33:01

Um, most of the time in early runs, it would, you know, the QA agent would kind of find a bug, um, and be like, "Uh, fix it later. Might take two weeks."
33:10

Um, uh, and then just kind of like be done with it. Um, so we actually had to spend an exorbitant amount of time like going through, um, trying to tune, you know, small layout bugs, edge cases, and, and kind of feeding that into the prompts.
33:27

I wish there was some kind of secret to, to actually doing this, but realistically the whole, uh, kind of art to building this system and making it good, uh, was kind of reading the traces.
33:37

Um, the primary debugging loop was this, and not necessarily running more experiments. It was reading what the agent actually did, um, finding where its judgment diverged from, um, ours as humans, and then tuning the prompt for that.
33:51

It was the same kind of muscle as reading kind of a stack trace. Um, um, one kind of tooling tip that we had was kind of piping agent transcripts, uh, into files, uh, kind of graphing them, uh, with another agent or having another agent kind of go through them, um, and then kind of update the prompts itself.
34:08

So you have some sort of like closing the loop even on just like building, uh, this harness out.
34:14

So the last thing I kind of wanted to talk about was, um, how to think about adjusting your harness as these models kind of get better in time. I think there's a lot of like discussion around whether harness design is kind of dead or null, especially with, you know, models at...
34:31

I mean, when I wrote this, it was just Opus 4.6, but even like Mythos, you know, level, level models. And I think the key thing that we note- noted is it's really important to get a feel for what the kind of spiky behaviors of any individual model are, and then try and adapt your harness to kind of
34:49

fill, fill the gaps. So, um, Andrew talked about this a bit, but, you know, context resetting between sessions. We kind of dropped that entirely. Opus 4.5 used to have really bad kind of context anxiety, um, whereas Opus 4.6 just, you know, didn't, um, uh, as part of a, pa- part of post-training there.
35:09

And so one continuous session and compaction was, was more than, more than enough to handle very long sessions. Sprint decomposition. Um, we don't have a very strong opinion on this, but it was something which was really, really critical to getting Opus 4.5 to work.
35:24

Um, but, uh, Opus 4.6 was able to kind of hold a, a two-hour continuous build coherently, uh, in a way without necessarily having to be force-fed one feature at a time.
35:35

Um, the cadence at which the evaluator should run. Previously, we were running it every single sprint per se, whereas now we were just running it at the end of a one-shot generation from the model and then passing back.
35:47

So the harness is still the same. We're just kind of simplifying the specific, uh, kind of loops, um, and the kind of recipe that kind of goes into it.
35:56

The lesson isn't necessarily our harness was wrong, but rather it was right for 4.5, the frontier moved, um, and we ran a simplified version, uh, to see how it worked.
36:08

So this is kind of what the final kind of setup kind of looks like today. Um, having that planner-generator-evaluator loop is still the kind of core of our system.
36:18

But you can see we kind of ditched a bunch of the other kind of, um-
36:24

Kind of components, uh, that made this slightly more complima- complicated than it had to be. Um, we also, as kind of mentioned, big fan of just using a file system for shared state, um, uh, instead of kind of leaning on context windows, uh, for very long-running agents in general.
36:39

And this is an example, uh, of the simplified harness running, um, with, uh, one of our latest models. Um, again, very, very expensive, but you can see it's actually roughly like half the cost of the previous runs,
36:56

um, just because, uh, uh, we're kind of doing things in a slightly more simplified manner. But it's still running over a very extended period of time.
37:04

And so this is an example of a DAW, which is basically just like a, a music-creating app, if you will. Um, the agent sets the tempo, a key, it lays down the melody, it builds the drum tracks.
37:18

This is the evaluator, um, actually going and, uh, testing the app itself. Um, we did actually listen to, like, the music in this. Um, obviously Claude can't hear at the moment, and so the music was pretty trash.
37:35

But the app was really good, uh, in general and pretty, pretty fleshed out, which, you know, a model ago, this is something which would never have worked. Um, but this is something which was possible with just a couple rounds.
37:48

Um, and this is kind of that, that METR curve which Andrew was talking about, uh, kind of really in, in action. And so I kind of wanted to close just by saying
37:58

you don't necessarily need, you know, our internal harness to, to go away and start thinking about this. We are constantly trying to ship bits of, you know, these primitives into Claude Code directly, but also there's nothing stopping you from just going ahead and building something similar to this, uh, kind of on your own.
38:14

So we just shipped, you know, auto mode is probably my favorite thing, um, for slightly more, you know, safe, safe YOLO, if you will, um, instead of running --dangerously-skip-permissions all the time.
38:24

Um, we already have custom sub-agents as a primitive, right? Your evaluator, your QA role, um, give it a harsh system prompt and a very detailed rubric. Um, Playwright MCP or Claude for Chrome MCP already extremely, extremely good, uh, at,
38:40

um, web app stuff or just use computer use if you're building kind of native apps. Um, and skills, again, a very nice way to package your kind of grading rubrics into your kind of general development flow.
38:52

Um, so yeah. Five things if you're kind of taking a photo, this is the, the slide I would say to, to, to kind of remember. Um, self-evaluation, very much a trap.
39:03

Just use an adversarial evaluator. Um, compaction doesn't necessarily-- uh, does not equal kind of coherence, right? Lossy summaries really drift. Um, structured handoffs, uh, and clean context, uh, are a very good pattern that we've seen.
39:18

Um, don't think that sub-subjective quality isn't gradable. If you have a strong view on what something should look like, um, then kind of force yourself to write it down.
39:28

Um, we found this made kind of a really massive difference, uh, to the quality of kind of apps, um, that a model was able to generate. And then kind of finally was really just, you know, sit with the model, read the traces.
39:40

Um, uh, only then can you kind of really know what bits, uh, of a scaffold to delete, um, what bits to keep, especially as the kind of frontier, uh, moves.
39:51

But yeah, that's it from me. Um, thank you very much for listening. [audience applauding]
40:01

And yeah, check out our blog post. Um, but wanted to just open up for Q&A in general because we've been yapping for like, you know, close to an hour now.
40:09

So, um, if you have any questions for me and Andrew, just fire away. We'll do our best to, to try and answer them.
40:15

Yeah.
40:19

Thank you. Uh, Joanne from Poolside. Uh, one question for you. When you, uh, improve the evaluator by, like, reading the logs and improving it, is that, uh, sort of like on a per project basis or more of a secret sauce that you reuse across project?
40:35

The goal, the goal was very much to try and do this in a way which was reusable, right? Like, I think anyone can tune this in a way that's, that's creating, you know, a very specific type of app.
40:45

That's fine. At that point, it's not that different from, you know, going ahead and just prompting Claude Code yourself and, and doing it, right? I think there were just-- the, the key was, like, what are the common patterns, uh, that you can kind of draw across the model weak points, right?
40:58

So talking to that kind of front-end design piece, we knew, like, what we thought good design would be, right? You could give examples like, this is what, you know, um, a, a really beautiful product looks like.
41:10

This is what AI slop looks like, right? Um, and that generalizes quite well. So yeah, this was all around web apps, but it could quite easily apply to, to other kind of things as well.
41:21

Thanks for... Oh, test. Uh, yeah. Uh, thank you for presentation. Very interesting. Uh, I-I was just wondering, what is your view on, um, uh, concept of dumb zone and smart zone of a model?
41:41

So I understand, like, before it was around forty percent. Now with one million contexts it's about one hundred K, is what I understand. And the way how I understood Ralph loop, Ralph loop was designed is to kind of negotiate this problem.
41:55

So basically, we're keeping the model always in a smart zone. So basically trying to, like, slice a task below a hundred, so it exe-execute the task within the hundred context zone.
42:06

And what I understand from your, your presentation, you kind of like advocating not to use it anymore because we can now rely on compaction handoffs and so on.
42:15

Is it like something you're suggesting to do, or would still-- is like a Ralph loop model still has its own place given the smart and dumb zone, uh, concept?
42:29

Yeah.
42:29

Yeah. Well, I suppose from Ash's presentation, um, and mine, you see that the one million context window is now GA, and so you have sort of a brig-bigger context to use.
42:39

Uh, the models are more agentic, so they can sort of maintain coherence for a longer period of time within that context window. And that actually, with the release of 4.6, we decided to move from new context windows to just a single long-running continuous session with compaction.
42:55

So I think, I mean, the-- whether or not you use multiple fresh sessions or just one long-running one is probably still up to your use case and your evals, um, depending on what you, you're seeing is working best.
43:08

But at least for sort of this general purpose, um, generator-evaluator pattern with Opus 4.6, we saw that it was possible to use a single session. I don't know if you wanna add to that.
43:18

I think, I think it's also just like a temporary problem, right? Like, context rot is, you know, a failing of like today's models to some extent, uh, and much less so than, you know, even just one model generation ago.
43:31

So is there a place for, for, um, you know, the type of thing which you're discussing? I think yes, uh, depending on use case, but, you know, it's not like a-- it's one of those pieces which I'd look at as like, okay, as soon...
43:44

You know, I'd be, I'd be kind of hunting for the model release where I can kind of strip it out. Let's put it that way.
43:53

I always have a lot of FOMO around Playwright. I mean, you said Playwright MCP. There's Playwright skills.
44:00

Do you-- Can you speak to how to improve the Playwright? 'Cause like, I imagine I would like to like have my browser open, and then I can see the model working through it, and then maybe I could steer it, you know-
44:13

Uh-huh.
44:13

... with a few tabs open. But like, yeah, what-- Is there some innovation there I'm missing out on? Or is, is Playwright MCP really... Do you recommend people use?
44:24

I mean, Playwright MCP or just use the Claude for Chrome MCP, which is like a, a slightly more robust thing, I guess, around browser control. I mean, I don't know why you wanna watch it do things.
44:36

I mean, you can, but I think that's like a, a trust gap, right, today. Like, you know, the whole point of what we're trying to get to do here is, is like
44:43

you set something off, uh, you trust it to do it, do the work, and test it, and you have the confidence that it's doing it correctly, and you come back to it.
44:50

Um, and that's where, you know, yes, there's gonna be some iteration at the beginning where you're like watching, reading the traces until you get to a point where you can trust it.
44:56

But, um, at least internally, right? Like when I'm, when I'm doing full stack app dev, um, I have got to a point now where I'm like, okay, with Opus 4.6, I can like reliably trust the model to go ahead, read, um, network errors, um, uh, uh, console errors, actually navigate an app, zoom in where it needs to.
45:20

Um, the vision is now good enough on these models that it can like identify overlapping text on elements and things like that, whereas that just wasn't the case, uh, uh, until realistically the last, you know, generation of models.
45:33

So yeah, I would, I would recommend. Um...
45:45

I'm curious, like with the generator-evaluator pattern, what happens-- Um, do you-- can you throw unlimited tokens at it or will it stop, uh, because the evaluator is not good enough?
45:57

Like, can you tell me more about that?
46:01

Sorry, do you mind clarifying? I kind of missed the beginning.
46:03

Yeah. So, okay. Let's say, um, I say, okay, create like a very cool game-
46:08

Mm-hmm.
46:09

um, with some features. You have the generator-evaluator pattern that, um, creates like contracts, builds the apps.
46:19

If I, um... Then it will give me back something, right? Um, can I restart it again and say like, okay, uh, make it better, I'm not, uh, happy about it and-
46:32

Mm-hmm.
46:32

-generator-evaluator will pick-- the pa-pattern will pick it up and make it better?
46:37

Yeah.
46:37

Or will the evaluator be not good at one point and just say like, this is it?
46:44

Um, I think that's... I mean, one, first of all, like if you want like a some, some level of human in the loop in this process, that's, that's like, you know, just implement hooks at some point, some point in this, in this loop.
46:55

Um, I think the bit which was kind of surprising to us, um, uh, was with this, this general pattern, and especially with the kind of 4.6 line of models, both Sonnet and Opus, it was extremely willing to like throw away everything.
47:11

You know, even if it had done kind of 10 passes at something,
47:14

it was kind of very happy to just like throw it all away and start from scratch if for some reason it wasn't able to like hill climb against the rubric of the evaluator in a kind of effective way.
47:24

Um, and so that's why kind of when we're kind of-- when we were playing with this kind of thing, we didn't naturally like lean towards having, um, some kind of resume or human-in-the-loop, uh, type intervention system, I guess.
47:40

And we didn't really observe-- We expected to, but we didn't really observe, um, that kind of behavior which you are talking about, where it kind of just like evaluates like, uh, just give up.
47:50

Let's just like pass it on, shall we say. Um, yeah. It was just much more willing to like throw away everything and, and restart, and that was just the behavior which we never saw when it was the generator itself almost kind of being proud of its own work and being like, "I'm not gonna restart this whole thing."
48:05

Um, so yeah. I mean, there, there's been an example which I've seen where the evaluator is like it kind of gets fed up and is like, 'Right, this approach you're taking just obviously isn't working.
48:15

Can you just like delete everything and restart?" Um, which I don't know about you guys, but vibe coding regularly, I often, I often do, uh, uh, as a human to like, you know, just benefit from fresh context windows, not have to deal with an, an already messy code base, et cetera.
48:29

So it's quite neat seeing models now also kind of, uh, get to that point.
48:35

I'd also just briefly add, obviously, you can then open that code base in Claude Code and continue where you left off. Um, sort of goes without saying. And I think we're generally thinking about what the workflow looks like, if it's sort of more back and forth, um, 'cause there's sort of the extreme of build me a really
48:52

complex gaming application that you don't know, is it gonna take three hours, is it gonna take twenty hours? Um, it's a bit unclear, so maybe there's sort of something in the middle that's, like, more of a, yeah, a feedback loop.
49:04

Hey, how you d- Oh. Hi. Um, I really like the idea that you have of, like, you know, there's a,
49:12

there's a human element here, whereas, like, you know, a PM, engineer, evaluator, um, PM role is a lot of the time, it's like scope creep and keeping the time going and stuff like that.
49:24

But you're just, like, letting this off. You're letting engineers go play in the sandbox-
49:28

Yeah
49:28

...for ages. [chuckles] Um, is there a harness loop that needs to go back to the planner eventually? Does it need to move again?
49:36

Um-
49:36

I feel like that's-
49:37

Well, maybe because we're engineers, we just decided, like, ah, screw the PM-
49:40

...we'll just shove it to the side.
49:40

Yeah, yeah
49:41

You guys need a PM. [chuckles]
49:44

We actually-- Well, this is where the kind of, like, that kind of contracting piece, uh, between the, the,
49:51

the kind of, uh, evaluator a-and the builder worked quite well. For context, in that, we typically, like, insert the main spec that was generated by, like, the PM per se, uh, into those sessions regularly, so that, you know, it's always a reference point, um, for, like, okay, this is what we're still actually trying to build.
50:10

And the main function of then the builder and the generator, uh, sorry, the builder and the evaluator is just to, like, figure out the exact feature set and tests and contracts per se that actually satisfy that spec.
50:22

Um, but the reason we don't is because we don't want the planner to be, like, a core part of this loop. It should be very high level. It should-- The, its purpose really is just kind of set out, like, kind of the hard outer lines of what this product could, could be.
50:42

Uh, but its job is not necessarily to come in and intervene and be like, "Actually, this is, like, an impossible feature. We should not do this," and, and, and edit itself.
50:50

Um, we kind of wanted to keep that context relationship between just, uh, just the builder and the generator. That being said, like, this loop, I've applied it in lots of different ways.
51:00

It doesn't have to just be, you know, one generator and one builder, right? Like, that adversarial kind of trade-off can be applied to, like, a workflow consisting of multiple separate agents, right?
51:10

Um, I don't know. It could, uh, if you're trying to do, um, I don't know, generate evals, let's say, you could use a similar harness. It would be like, hey, generate a, uh, it could be, like, planner, generate a synthetic, a generator for synthetic datasets, right?
51:27

Uh, with a QA agent. Then hand off to, uh, like an integrator, which, like, actually wires up something, also has a QA agent, then has, like, a final kind of a...
51:35

You can basically add this kind of generator-evaluator thing into a multi-step workflow. Uh, where each, like, builder maybe has, like, a slightly different function per se as part of a, a longer workflow.
51:45

So, there are different ways in which you kind of keep things on track depending on the task and break down, uh, this, this general pattern into slightly more specified,
51:57

you know, uh, tasks or workflows, if that makes sense.
52:01

Hi. Can you-- Uh, you mentioned that, uh, some of the later tasks could not possibly be done by an earlier model. Can you talk a little bit about your process comparing the tasks on the different models?
52:14

Like, do you fire off the same task on Opus 4.6, Opus 4.5, Sonnet? Or is this sort of artisanal, uh, co-evolving, uh, harness model, uh, set up, uh, obviating that?
52:32

Yeah, I mean, I suppose we walk through the history a little bit, and if you look at, say, the first blog post on long run-running agents versus the more recent one, um, there are some pretty significant differences there.
52:43

You know, one being what we were just discussing, that the initializer agent would build this super comprehensive spec of, say, two hundred different features. Um, and then, um, in, then the loop would have to actually go and execute against every single one of those features, which may lead to, say, incorrect design decisions, but it's sort of forced
53:02

into that behavior. Whereas I think now you're able to have sort of a more generic creative direction set with, say, Opus 4.6, and then just having this, this loop of the generator-evaluator.
53:14

But it, it does... Yeah, your model selection does inform your harness design very much so. Um, of course, in a perfect world, you could just sort of throw everything at, say, Opus 4.6, but if you have cost concerns, for example, maybe you do use Opus 4.6 for planning and then Sonnet 4.6 for, for the coding or the
53:33

execution. That's something that we, we tend to see quite frequently. Um, but again, if you're building specific sub-agents for each of these, you probably wanna have some evaluations to be able to understand for that model and that prompt how it's performing against that task, and then just optimize.
53:50

Do you have any advice on moving beyond sort of these one-shot applications to long-lived products where you're looking to make changes days, weeks later? And what sort of artifacts you need to persist to future instances to be able to know what has come before, what can I change, what should I change?
54:08

Yeah. It's something which we're working on. Um,
54:11

like, right now, like, we use, like, similar patterns for just a bunch of random stuff internally, shall we say. And so at the moment it's like, set this thing off, it's running, you know, um, on, uh, a remote server somewhere, um, and I'll just come back and check it, like, after this talk, let's say.
54:27

And then I kind of iterate on it kind of manually, uh, in code directly, like polish any rough edges, that kind of thing. I think-
54:36

In terms of the way that you're actually, like, setting up this harness, just having, um... This is why we kind of, uh, default to kind of using a file system as state, uh, for this kind of loop.
54:47

One, because it's just very easy for another model to come up and, and grep through and, and pick up what, what's been going. But one thing which I like to do is kind of embed little bits of prompting, uh, throughout this kind of loop, which basically tells it to write kind of learnings and state to, uh, some
55:04

kind of, uh, JSON file because the model doesn't kind of overwrite that too much. Um, and so the nice thing, uh, about that is you're basically just leaving, like, breadcrumbs for another model to come and pick up.
55:16

So honestly, the, the key thing for me is, like, how do I instruct this, this harness to leave crumbs for a human to come in and then use Claude Code on top of?
55:26

So generally it's like, hey, uh, the shape of that file might be like, uh, tried this, uh, evaluator found this bug, uh, implemented this fix, this fix worked. Yes, tick, and then continue.
55:39

And you have kind of like a timestamped, uh, kind of time log, if you will, of like everything the model has tried, the fix it's made and the final state.
55:48

Um, and then also, uh, having some sort of live updating kind of set of docs, if you will. Just very high level, here's the file structure. And then those two files, to be honest, are more than enough for Claude Code and a human to come in and start iterating on the app with.
56:04

But that's what we're doing at the moment.
56:06

Mm-hmm.
56:13

Perfect. Um, so it's very interesting to hear the-- Or yeah, first of all, congrats on the presentation. [chuckles]
56:21

Thank you.
56:21

Um, and then I was wondering, there are kind of two approaches, like you have the agent team where multiple agents interact with each other, and then the explicit generator critic, the setup.
56:34

But what are-- Like, because in sense, like the agent team has the same setup where the main agent instructs someone and then can act as a critic for the sub-agent.
56:47

But what are the current failure modes that causes us to still need the specific generator critic harness instead of just the agent, uh, team itself? And then what's your estimate of how many model generations we would need to just
57:05

completely rely on the agent team? Uh...
57:09

Mm-hmm. Maybe-
57:11

Is it clear?
57:11

I mean, I can-
57:12

Yeah.
57:12

I can sort of address the first aspect of that. So I mean, one of the limitation of-- Firstly, Claude Code is, is using the same harness that, that is the Agent SDK.
57:22

So you can-- technically you should be able to build this type of a pattern into Claude Code. Um, agent teams is a useful framework for potentially doing that because you could, say, have the, the generator and the evaluator sort of intercommunicating, or maybe it's the generator as sort of the main agent and, and the evaluator as, say,
57:42

a member of, of the agent team. Um, but I think it's, it's sort of evolved more so from that first blog post that I showed. I think that was like the, the result of that to some extent, to try and make that more generally available.
57:56

Um, but one of the things you're limited by obviously is like Claude C-Code would just have to run on your machine. I think with the Agent SDK, you can also just run it in more of a cloud environment and a sandbox environment for long periods of time and, um, without it, it failing, um, or you having to
58:12

run like caffeinate on your machine. Um, but I think, yeah, Claude Code is a good testing ground for building out any of these types of harnesses to experiment and explore and see what works before maybe you build it into the Agent SDK and then actually deploy it as its own application.
58:29

Um, and yeah, I, I mean, again, I would just experiment, see if agent teams is something that makes sense for you or if maybe just using regular sub-agents or some other framing of it, it works better.
58:40

But yeah-
58:41

Yeah, I think-
58:41

... people are using agent teams like a, a ton. I don, I don't know if you-
58:45

Yeah, well, this is the thing is like I don't think we have like a super strongly opinioned viewpoint on like, um, what is the best at any, you know, sort of at any given moment in time.
58:54

That's why Boris always like updates his tweets like, "This is what I'm doing now." Um, like agent teams was something which a bunch of people loved internally. Um, uh, and so we were like, "Okay, let's ship it.
59:06

Let's see what people think about it in the field." Um, I'm not saying we will, but it, you know, we regularly unship things as well. Um, and I do see the generator evaluator kind of pattern as like a, a subset of that, like teams approach to thinking about sub-agent design.
59:21

Um, not necessarily like contradictory to it per se. You know, you can imagine like, you know, classic way in which teams breaks down is like, you know, front end, back end, um, some sort of integrator between them, like sub-agents.
59:32

Each of those probably deserve their own kind of critic, um, uh, a kind of agent pairing with them, for example. Um, so you can kind of see how the two concepts like overlap.
59:42

Um, just the general idea behind this is, you know, most people when they're running Claude Code at the moment, their goal isn't to like one-shot an app over like six hours.
59:53

And so that isn't necessarily the primitive which we like by default like ship, uh, there. Um, so yeah.
1:00:03

Yeah. Sorry. One thing I was wondering, have you also tried like a critic that gets the context of the generator, then you feel like if it has some clue about the traces of the agent or like the executor?
1:00:19

Yeah.
1:00:19

Is that currently the case in the, the critic?
1:00:22

Uh, we u- we use like a handoff plan. I, I would be very hesitant of that. We did try this, but this is the whole like muddying of, of like thoughts between the two, two model streams.
1:00:34

I think it's actually much more effective to just let it judge the output, um, and just provide. Instead of being like Hey, you made a misstep when building this by doing X, and that's what's resulting in this issue.
1:00:45

It's much more effective to just have the evaluator to be like, this is an issue, and then let the generator purely reflect on its own work and then try and figure out how to fix that issue.
1:00:53

Um, otherwise you kind of just see-- We found that
1:00:58

it's very easy for the model to, like, kid itself if that something is working or not, and that feed into the evaluator as well.
1:01:04

Last note on that. I think it would then be interesting if you-- for the training team-
1:01:11

Yeah.
1:01:11

If you could train, like, the, the generator to predict what a critic currently said.
1:01:16

Yeah.
1:01:16

Like to, to have it be more honest about what it did and stuff.
1:01:20

Maybe we'll work on that. [chuckles]
1:01:25

Um, I want- I wanted to ask more about traceability. Like I use, um, superpowers or like my own prompts to generate like multiple sub-agents to implement my, let's say my software or app.
1:01:39

But what happens is like I don't really know... I want to go back and see where it actually went wrong even. But then I'm not able to figure out how to find those traces.
1:01:49

How-- What do you use for traceability is my question. When you have so many, like five, six agents running in background like, um, yeah.
1:01:57

Um, to be honest, a lot of it is just reading through traces by hand. Um, we do a lot of that, I would say at Anthropic in general, just like reading through traces by hand.
1:02:09

Um, we also just like have, you know, hacked together various things where we, you know, point Claude at, uh, a bunch of traces, um, uh, with some custom prompts, uh, to try and identify like issues with the loop, like this is where it veered off and whatnot.
1:02:25

Um, we kind of use that as like a first pass, I would say maybe to just kind of like see where something w-w-where like where something might have gone wrong.
1:02:33

But to be honest, by far and away the, the, the best approach at least that we use internally is just, just reading, reading the traces by hand. Um, only then do you kind of like truly get to kind of relate to what the model is trying to actually do.
1:02:45

Um, yeah.
1:02:51

Thanks for the talk. Um, I have a few questions. Uh, first of all, how do you measure the quality of a harness-agent pair? Is it-- It feels like a vibe check, like it's a greenfield, uh, let's build an app.
1:03:05

Mm-hmm.
1:03:05

Um, but let's say you're, uh, you're going into a new project, maybe brownfield. Um, it feels like a vibe check or some kind of art. Can you make it more scientific, or is that just not feasible?
1:03:19

I mean, the way that we've thought about it at least, right, is like we specify the rubrics in kind of extreme detail at the kind of generator and evaluator level, right?
1:03:28

So we talked about, for example, those four kind of criteria. That's very high level, the rubric which we use for like design taste, let's say. And so
1:03:36

we set those up for various bits of this app, right? So that can be just for the design element, maybe another piece for like how we think about, um, uh, kind of API design, let's say, um, um, code quality, whatever.
1:03:50

And we kind of use those as the, uh, kind of various sort of rubrics which we're hill climbing against, right? And then the evaluator's job is to, you know, encourage the builder to hill climb against those.
1:04:02

And so for any given app or output, we have like a signal of this is where the model started on those, those kind of criteria, and this is where we've kind of ended up.
1:04:12

Now, that's less useful for like kind of, like you said, working on, um, kind of newer code bases, but it still applies, right? Like you could point-- You just have to start the loop a different way.
1:04:22

Um, you would just point the evaluator at a given code base, um, and be like, "This is where we are now." And then, uh, uh give it the, the spec of what you're trying to achieve, and then let the loop kind of iterate against those kind of criteria.
1:04:36

So there isn't like a necessarily a one set of evals at the very end. It's kind of like here are the criteria for what we think good looks like, then letting the, uh, evaluator and the generator come up with a set of kind of tests, uh, or contracts that it needs to satisfy, and then letting it, just
1:04:52

as the harness, hill climb against those. Um, that's not super comparable across different products and runs, um, but it's, it's very useful for, for, yeah, within a product or run.
1:05:03

Also this, um, this particular pattern is great for greenfield, like you said, but it's quite opinionated. You know, it might be using React, like Postgres as a database and Node on the back end, but your brownfield app might be using something totally different.
1:05:16

Or the rubric that we've created for what we think, you know, good sort of design patterns are would-- might be totally different in your project. So I think that's why we're proposing this as more of a pattern that you would then, um, tailor towards, you know, your application.
1:05:31

Thanks. Um, one follow-up question. Oh, does it work? Yeah.
1:05:35

It can.
1:05:35

Um, do you use, uh-- Do you like direct the harness individually, and how do you cooperate as a team on that? I find it's very hard to like, uh, when I share my screen and I'm working conversationally, it's very hard for people to keep up.
1:05:51

And the other way around, I find it cumbersome to dictate what to prompt. Uh, how do you cooperate as a team? Do you have like team-owned harnesses?
1:06:01

Um...
1:06:04

Is it maybe a good feature for Claude Code? [laughs]
1:06:07

Um, yeah, maybe. May-- I, I think we, we probably do have work to do on that, right? Like, I think like, um,
1:06:17

quite often what happens internally is like, you know, people come up with these ideas, and then they're generally quite bottoms-up adopted by different teams. And, um, it's then the job of the kind of original, you know, uh, idea holder, shall we say, which was Prithvi in this case, to kind of maintain it and make it kind of
1:06:32

composable and generalizable for different teams. And different teams will adapt it and, and you know, uh, make it useful for like their section of a code base, let's say.
1:06:41

Um, but we don't have any like Good things in that terms. I think like, you know, even just observability, like some of the people talked about, right? Is like a, um, generally speaking, a thing which is not fully solved yet for these, like, ultra-long running, uh, agents.
1:06:56

And yeah, interesting area of kind of greenfield software to explore.
1:07:02

Yeah, that is, that is an interesting one, whether it should be sort of a collaborative experience in, in Claude Code or even Claude.ai. I think in just leveraging software engineering best practices with version control and making your commits and pull requests, or if you're working on your own using something like Git worktrees so that you're not overriding
1:07:20

the f- the file system on multiple different features all makes sense. But yeah, I think when it comes to collaboration, maybe it's something that, you know, doesn't happen quite as much because people just build these projects, as Ash said, from the ground up and then sort of pr- you know, pr-present them to the rest of the company.
1:07:40

Um, hi. Uh, Jose from Mercedes-Benz Research and Development here. Hi, thanks for the talk. Um, while looking at it, I thought, okay, it looks a lot like a Scrum team, a feature team working l- for longer times, uh, on a, on a product.
1:07:57

And I was thinking, um, how does human-in-the-loop look like in that scenario? Um, because it-- you have-- you had this kind of sprint. Uh, have you thought about a sprint review kind of moment where y- where you, as a human, get asked, "Oh, hey, here's what we built the last two hours."
1:08:17

Yeah.
1:08:18

How's it looking like for you?
1:08:20

Yeah. Should we subject our agents the same trauma that like engineers go through, [laughing] um, of, of, of, of Scrum review? Uh,
1:08:29

I mean, like the whole point of this general-- the general idea which behind this talk and also what we're trying to do is like trying to be as like AGI-pilled as possible, right?
1:08:37

Like how do we build harnesses where we don't need a human-in-the-loop, right? Like, what does that look like? Are we using this today for everything? Obviously not, right? Um, uh, but the goal is, you know, this is, this is a technique or a pattern which should extend very nicely such that you, you don't have a human-in-the-loop for
1:08:52

most things. If you did, right, it's like, uh, you know, hooks is probably the main primitive, uh, to just basically inject, uh, uh, given some sort of specific type of stop condition, let's say, with an evaluator, um, uh, to basically like hand back to human, allow some kind of developer message input, and then continue the loop, uh,
1:09:11

would be like kind of the simple way to implement it. But yeah, to be honest, we're kind of exploring this from a
1:09:20

what can we do fully autonomously kind of approach, as opposed to thinking this as like, here's Claude Code and, and like, how do we make this like, you know, more powerful per se?
1:09:29

It's very much like a kind of more greenfield exploration of agent design.
1:09:33

No, no, of course. It's just like, um, if, if, if I would get the chance to review it maybe a few hours in, then I might be able to steer it in a ba- way better way-
1:09:44

Yeah
1:09:44

... so that eight hours later, it's more like the one kind of project I would like to have.
1:09:50

Yeah. I mean, I get what you're saying. I think the question then is, is like, should that be like a permanent feature of the harness, or is that just like a, a, a, a thing which you should have like kind of basically prompted around when building the harness, right?
1:10:02

So we would have that, right? We would run this, this, this harness on loop, um, and we would have, you know, we might spin up like ten generations of different things, and like three of them succeed and seven of them fail in like random ways.
1:10:15

And then we would just sit down with those seven, read through them, uh, adjust the prompting of the main harness, and then, and then try again. And until we get to a point where we're like quite happy leaving it run, uh, leaving it to run fully autonomously.
1:10:25

So ultimately, that's still the end goal for us, as opposed to being like
1:10:29

basically giving up on the harness and being like, "Okay, we'll just insert a human here to, to like cover for any kind of steerability issues and stuff." We'd rather embed that and bake that into the harness itself, um, in the first place.
1:10:46

Have you used this to build anything like sort of like non-greenfield or I guess like production, like anything in Claude Code itself? Or like h-have you used it for actual features and, and seeing it to the end?
1:11:00

Um, I think, I mean, this does mostly extend to greenfield projects. I think for brownfield, maybe you do need a little bit more control, um, as you're starting to build out your own rubrics and, and patterns.
1:11:13

Um, I mean, what we're seeing in brownfield is that if you look at the whole software development life s- life cycles, not just the coding aspects, that people are starting to use something like Claude Code for, it might be, say, there's like autonomous monitoring happen- happening.
1:11:28

Um, and then that could feed into, say, generating some kind of like issue or, or feature request that could then just feed into, um, an agent that would then go through to make the pull request, and then there's sort of a pull review, um, already happening, and then maybe you're just reviewing that before you actually merge.
1:11:48

So I think there, there are other ways to automate the whole software development life cycle, um, uh, in a brownfield project. But I think this particular pattern maybe without a lot of testing within your project and building, like customizing it for your project, it's probably more suited towards brand-new applications.
1:12:06

Have, have you built any greenfield apps that like, I don't know, like an internal tooling or, or anything like that that you've been using? Like not just a demo, sort of like...
1:12:14

Yeah. Um, to be frank, I can't really like talk to like internal tooling too much, but a good anecdote of this was, um,
1:12:23

like a lot of the, the new and fun stuff that you see in Claude Code will, will like, um, uh, when I'm speaking to the team and working with them on, on stuff,
1:12:33

use a lot of the lessons from this per se. Like in, in like even just general hands-on, uh, Claude Code usage, the way that they prompt, you know, the main Uh, model to, to spin up a sub-agent, let's say, and, and, and go after something.
1:12:48

Or as kind of Andrew said, right, in kind of monitoring and bug-fixing loops. Like, you know, when generating a fix, like should you have a separate evaluator and a generator go after the same thing?
1:12:58

So a lot of these principles apply. Um, is it like, you know, one for one this? Maybe not, but it's like taking the good bits of this or whatever you think is, is kind of applicable to a certain space and field, and then kind of running with it in your own way.
1:13:12

Thank you.
1:13:25

Hi. When you say reading the traces, is that literally just like the raw output, or is this something more specific you've prompted it to like write this to file, these are the sorts of things I care about and I wanna see?
1:13:36

No, you gotta read the whole thing. Read the whole thing. I do think it's like a, a really important skill when building agents in general, is to like empathize as much with the model.
1:13:45

Um, this was like-- There's an interesting, uh, uh, anecdote which we used when we were building, for example, the agent harness for Claude for Chrome, um, which is our kind of browser use thing.
1:13:56

Um, and we would run this like experiment where like imagine if, you know, you were trying to navigate a webpage and click around where like, you know, you're effectively doing it with your eyes closed, and like every ten seconds you just opened it to see like a static page and then closed it again, and then had to
1:14:09

like do things. Um, and like really putting yourself in the shoes of the model, um,
1:14:15

is kind of like this kind of empathetic skill set which you need to develop. Um, and the only way to really do that is to like spend as much time with these models, but also, yeah, reading through line by line being like, "Oh, why did it think this?
1:14:27

Oh, I can kinda see why it did that." And then kind of adjusting the way you instruct it next time to, to do better. Um, but that's why I think Claude for Chrome is very good with just really just like spending a lot of time as a team, uh, closing our eyes [chuckles] and trying to navigate web pages,
1:14:41

for example. So, um, yeah.
1:14:44

Mm-hmm. Yeah, and I think then actually taking those learnings and putting them into, say, your prompt templates or your CLAUDE.md, or building a skill, or just generally understanding how to sort of avoid that type of behavior in the future.
1:15:00

I know Claude Code now has auto memory for sessions as well, so it's sort of constantly memorizing little things as it goes. Um, but yeah, you can learn quite quickly from reading some traces, like where things might be going wrong.
1:15:13

Cool. Should we wrap up there? Um, I think we have a few minutes left, but we'll be around in general in case you guys wanna ask any questions or just chat.
1:15:20

But otherwise, thanks for coming down.
