Source: "Another review of the potato/pstack skills", YouTube video https://www.youtube.com/watch?v=lUhXa8GiXns. GitHub link for the skills: https://github.com/cursor/plugins/tree/main/pstack. Video describes Lauren Tan's pstack set of skills. Transcript pasted into the chat by Boroon on 1 November 2026. Saved verbatim as pasted, including chapter headings.

---

Pstack Intro and Setup
0:00
So this is Lauren Tan, ninja engineer.
0:02
She's worked at Netflix. She's a member
0:04
of the core React team. You might have
0:05
heard of React and principal engineer at
0:07
SpaceX and also Cursor. If you're
0:09
building coding agents or using any kind
0:11
of software factory, you have to check
0:12
out her set of skills. It's basically a
0:15
senior engineer's brain extracted into
0:17
one stack. Even our friend Theo has done
0:20
a deep dive on how awesome her skills
0:22
are. So even if you don't end up using
0:24
Pstack, just reading them will give you
0:26
a breakdown of how a serious agent
0:28
practitioner works at scale. So in just
0:30
one afternoon, I created this skill
0:32
manager called Molton Base to manage all
0:34
my skills across my various different
0:35
agents. I'll take you through some of
0:37
that process and a breakdown of all the
0:39
noteworthy skills. This is a couple of
0:41
minutes that's really going to help you
0:42
improve your work with agents. Pstack is
0:44
broken down into all of her principles
0:47
and engineering rules. Then we've got
0:48
the playbooks which you can think of as
0:50
operating procedures so the agent knows
0:52
what to do next. And then all the
0:54
individual skills and slash commands
0:56
that do all the work even after using
0:58
agents for 2 years and building my own
0:59
set of skills. There are a few in here
1:01
that are absolutely getting added to my
1:03
default list. So you can run pack
1:06
anywhere you want. Cursor claw codeex.
1:08
You can find the official repo from
1:10
cursor and lauren at plugins pack at
1:12
ccursor. I'll leave the link in the
1:14
description down below. And it's as
1:15
simple as just typing in slash addplugin
1:18
pstack when you're in cursor. If you
1:19
want to run this on claw codeex open
1:22
code, I found this not official repo by
1:24
Michael Dener. He's done the porting
1:26
into each one of the agents. So you can
1:28
actually run that by installing it from
1:30
the plug-in marketplaces.
PStack Skills
1:34
So the heart of the Pstack is potato
1:36
mode. It's essentially a router that
1:38
helps you decide which one of the 20
1:40
plus skills you should use first. So
1:42
what we've got here in our skill tree is
1:44
essentially 22 playbooks which gives a
1:47
nice set of examples here for different
1:48
use cases along with each one of the
1:50
prompts. I always love an opportunity to
1:52
build some new software. I haven't found
1:54
a good skill manager that I like using.
1:56
So let's go and build our own. So I've
1:58
given potato mode a prompt here and
2:00
let's see which one of its skills it
2:01
uses to kick this off. So the [snorts]
2:03
first thing we see here is potato mode
2:04
actually rooted this to a figure it out
2:07
playbook. If you're expecting something
2:08
like BMAD superpowers or OpenSpec, this
2:11
isn't necessarily designed for spec and
2:13
planning. This is meant to be operated
2:15
on an established codebase. Laurens's
2:17
personal take on this is I don't believe
2:20
in planning. The best spec is the code.
2:22
So there's deliberately no planning
2:24
skill baked into Pstack. Now you can
2:27
already see the arena skill is in place.
2:29
So we have a design idea distributed
2:31
between Claude, GPT, Grock, and Claude
2:34
Opus 5. There goes the token budget. If
2:37
you have a critical feature to develop
2:38
and tokens are not an issue, you can run
2:40
arena. It is it pits three or four
2:42
different agents against the same
2:44
problem and it takes the best parts of
2:46
each and wraps them into a final commit.
2:49
And it's something that cursor had baked
2:50
in 6 months ago and they later removed.
2:52
So basically having them all fight it
2:54
out to the best design and then picking
2:56
the best parts of each design. So based
2:57
on what each one of the sub agents
2:59
learned while working on the problem,
3:01
Arena decides to either graft or reject.
3:04
Now, similar to that, we have the idea
3:06
of swarm. It's the idea that again,
3:08
you've got parallel workers, but you
3:10
give them different slices of the
3:12
problem and then you pull it all back
3:13
into one aggregated report. Pstack is
3:16
designed so you get fearless
3:17
parallelism. If you're working across
3:18
feature branches, work trees, etc. Even
3:20
if you're using arena or swarm, it's
3:22
aggregating all of your work together,
3:24
making sure there's no overlaps. Well,
3:26
that's the idea in principle. It is a
3:28
big claim. I haven't used it enough to
3:30
say that that is actually the case, but
3:31
you can see how the principles are baked
3:33
in to allow for it. Using its TDD skill
3:36
or testdriven development, it went and
3:37
created a bunch of unit tests first and
3:39
then made sure they passed before
3:41
proceeding. So this skill I particularly
3:43
like why. So the Y skill is really cool.
3:46
Instead of just checking the transcript
3:48
for the project, it basically runs
3:50
through all the different MCPS and CLI
3:53
that you have that are relevant to the
3:54
project. It might check product
3:56
information in Post Hog. might go to a
3:58
conversation thread in Slack about why a
4:00
feature was implemented. It might pull
4:02
logs from sentry to get a full big
4:04
picture of decision records or adors as
4:07
to why something was done. Definitely
4:09
stealing this one. So just like potato
Sponsor OpenRouter
4:11
mode is a router for all the skills in
4:13
Pstack, open router is pretty much a
4:16
router for all the models you could
4:17
possibly want to use. Basically, one API
4:20
key and one bill gets you all the text,
4:22
video, voice, and image models you could
4:25
possibly want under one API endpoint.
4:28
There are so many reasons why that is
4:30
awesome, but for today, here's just one.
4:32
I get so tired of logging into different
4:34
dashboards, figuring out what API keys I
4:37
have, switching around providers for
4:39
video and images, and not to mention, my
4:40
poor agent has to manage so many
4:42
different APIs. So, I went and built a
4:44
CLI that interacts with Open Routers
4:46
API. I want to be able to generate
4:47
images, videos, and voice using any
4:49
provider using claw code, cursor or
4:51
codecs and create a singular skill that
4:53
can invoke the CLI. So basically, I got
4:55
my agent to build a CLI that connects to
4:57
Open Router along with a set of skills
4:59
so I can generate images, videos, text,
5:01
and even audio. I just need to grab one
5:04
API key. So then I can use my new skill
5:06
and CLI via Open Router's API to do
5:09
things like generate a video of a load
5:10
of potatoes rotating around my head
5:12
using Cadream. And just like that, we
5:14
have a head full of potatoes. Rob Shocks
5:16
viewers can check out Open Router via
5:18
the link in the description down below.
5:19
Next up in terms of usefulness, we have
Robs Favourite Skills
5:21
recall. So recall is fantastic for when
5:24
you want to pick up on a project that
5:25
you've just left off. Maybe it's been a
5:27
week or so, you're trying to remember
5:28
where you're at. It will scan through
5:30
all the transcripts. It'll even use the
5:32
Y skill to go and check your MCPS like
5:34
Notion Linear or Post Hog to find out
5:37
where we're at and what we need to do
5:39
next. To be honest, just reading through
5:41
the skills themselves, there's some
5:43
great learning in here for developers.
5:45
some fantastic patterns that are really
5:46
worth knowing. So once the code is
5:48
actually developed, we're into the
5:49
validation stage. So we have
5:51
interrogate. So with interrogate, you're
5:53
basically getting two or three different
5:55
models to go and interrogate or doublech
5:58
checkck the code against its standards.
6:00
Multiple different models review the
6:01
same code and they all come back with
6:03
their opinions. Now, you're going to
6:04
burn a ton of tokens with some of these
6:06
skills. But inevitably, if what you're
6:08
looking for is the highest and strictest
6:09
code quality, the token count probably
6:12
isn't going to matter to you here. This
6:14
one I absolutely love. It's the create
6:16
verification skill. So basically, it
6:19
created its own scripted way to prove
6:22
out the app behavior. We have to delve
6:24
into the root, multiple different
6:25
projects and setups. We have to scan
6:27
continuously to make sure that
6:29
everything's updated. There is a large
6:31
surface area for this app to appear to
6:33
be working but actually be fundamentally
6:35
broken or giving us the wrong data. So
6:37
it went and created a set of
6:39
verification scripts and cross checks.
6:41
When you're dealing with
6:42
non-deterministic agents, this kind of
6:44
verification step is just so valuable.
6:46
We also have a maintain verification
6:49
skill. So oftent time as the app
6:51
develops, the script or verifier that
6:53
you've set up is going to diverge from
6:55
the development. So running this skill
6:57
will actually go back and make sure that
6:59
it gets updated. The unslop skill is an
7:01
absolute gift if you use your agents to
7:03
do any form of riding with the purpose
7:05
of killing and removing all those
7:07
annoying phrases like pivotal moment,
7:09
crucial, delve, enduring, and the
7:12
controversial one, getting rid of em
7:14
dashes entirely. I actually like em
7:16
dashes. I used them a long time before
7:18
AI came along. Sad to see them go, but
7:20
inevitably it seems like a big tell for
7:22
people that AI is used when you see that
7:24
little line. Let's say I've been running
7:25
a load of agents in parallel all morning
7:27
and my brain is just coming to a halt.
7:29
This is just too much for me to gro. I
7:31
can actually run the bro skill, which
7:33
basically restates the last message in
7:35
plain human language with no jargon. So,
7:38
let's give it a go. This bro skill is an
7:40
absolute gift for clarity, particularly
7:42
when your brain has been burning hard on
7:44
10 different agents.
PStack Methodology
7:49
So, we can learn an awful lot about
7:51
Pstack, how it works from the show me
7:53
your work skill. So, I ran this on the
7:55
first invocation of that one prompt. Now
7:58
remember this whole thing was one shot
8:00
of that one single prompt we started
8:02
with. So just like any good engineer it
8:04
started with some probing. So a probe
8:06
can be a quick test to see if what we're
8:08
trying to achieve is even possible.
8:10
We're not going to build the whole app.
8:11
We're just going to write a small script
8:13
and just investigate to see if it is
8:15
actually possible. So the initial frame
8:17
is understanding the requirements and
8:18
the constraints of the ask. So in this
8:20
case we're saying that we want it to
8:22
operate on Mac but then eventually on
8:23
other systems. So it's able to create a
8:25
frame around what needs to be built.
8:27
Next up, we did some basic scaffolding
8:29
for the app before we moved into the
8:31
arena stage where we had four parallel
8:33
agents working on the problem. So this
8:36
one is particularly interesting. Design
8:38
changes forced by reality. Now this can
8:41
sometimes be the problem with doing too
8:43
much planning up front. When the agent
8:46
creates this very detailed plan, it
8:48
hasn't actually dealt with reality yet.
8:50
It's only as we build and develop that
8:52
our assumptions get broken and we have
8:54
to rework the problem and come up with a
8:56
new plan on the fly. In phase E here, we
8:59
have all the verification testing and
9:01
then we finish up with our audit. Now,
9:03
this is why verification is so
9:05
important. The agent had realized it had
9:07
hallucinated some of the details. It
9:10
caught three false claims that it was
9:11
able to correct.
Lead Principles of Agent Engineering
9:16
So, let's take a look at the key
9:17
principles. Number one, laziness
9:19
protocol. Absolutely love this one. When
9:21
refactoring our code, let's look to
9:23
delete code if possible and make this a
9:25
whole lot simpler rather than adding
9:27
more code. And let's just aim for the
9:29
smallest change to get the job done
9:31
because inevitably that leads to far
9:32
more maintainable code later on. So
9:35
redesigning from first principles. So as
9:38
your project grows and you're adding
9:39
more features, the agent might decide to
9:41
bolt on the next feature or
9:43
functionality. What redesigning from
9:45
first principle is doing is basically
9:47
saying that let's imagine that we're
9:49
adding this feature from day one. How
9:51
would you look at the code structure?
9:53
How would you have designed the
9:54
scaffolding the database to structures
9:56
in order to make sure this was more of a
9:58
native feature? So this might actually
10:00
involve removing some structures and
10:02
some code in order to get to our happy
10:05
place. So again from Lauren, the goal
10:07
isn't more code, it's maximum impact
10:10
with the least amount of code.
10:11
Minimizing reader load. We're all
10:13
getting so sick of these huge PRs
10:16
written by agents with disjointed code
10:18
across several abstractions and modules.
10:20
The idea here is that we minimize the
10:22
reader load. We keep things super simple
10:24
with the minimum amount of abstractions.
10:26
Exhaust the design space. So this is
10:28
very much where the agent arena comes
10:30
in. We can have multiple different
10:31
models and agents working on the same
10:33
problem. Come up with the best of all
10:35
and then graft the best parts into our
10:37
final commit. In my course, I teach this
10:39
thing called design mode where we
10:41
actually just scaffold out a couple of
10:42
different variations of what the
10:44
interface might look like without any
10:45
database or code in the background so we
10:47
can come up with the best option for
10:49
design before we move forward. Next
10:50
principle is build a lever. So if you're
10:53
going to be doing something with your
10:54
agent by hand multiple times, why don't
10:56
you build a tool for that? It could be a
10:58
CLI. It could be a script that does the
11:01
same verification over and over and
11:02
again, which we see via the verification
11:04
skill. Lauren has also baked in some
11:06
great disciplines here. To be honest,
11:08
you would hope that a model like Fable
11:10
or Astra would start to think about and
11:12
bake these things in naturally, but when
11:14
it comes to verification steps, there is
11:16
no harm in having these kind of
11:18
disciplines applied after the fact. One
11:21
of the biggest principles that flows
11:22
through the entire stack is
11:25
verification. Having it compile and go
11:27
green on tests is not the same as
11:29
actually testing and proving it works in
11:31
terms of a real artifact. by deeper
11:33
verification, whether that's via
11:34
computer use or end to end testing.
11:36
Guard the context window and never block
11:39
the human. You can see this throughout
11:40
the skills and the playbooks. The
11:42
central context window is key. It's
11:45
important. How do we offload slices of
11:47
the task to sub aents? They've got their
11:50
own unique context windows to do their
11:52
work and then they report back to the
PStack vs No Stack
11:53
central thread. The combined skills and
11:55
methodology while costing a lot more in
11:57
terms of time and tokens have led to a
12:00
much more hardened application. Using
12:03
Fable 5.1 without any plan mode and
12:06
without any skills attached, it took
12:08
about 30 minutes to get the project
12:10
done. Using the P stack, it took 1 hour.
12:13
So twice the amount of time. However,
12:16
the difference between the two projects
12:17
is substantial. Now let's be very clear.
12:20
Pstack as a set of machinery and skills
12:22
in your repo is going to cost you a lot
12:24
more money. All of this validation,
12:26
verification, and swarms means a lot of
12:29
token burning. You might not need to
12:31
throw the potato at every single project
12:33
that you have, but at least you have an
12:35
idea of what it's good at and where it
12:36
can be used. If you're making small
12:38
design changes or working on the
12:40
front-end UI, you probably don't need to
12:42
be using this. So, if you're subscribed,
12:44
and I hope you are, I've been building
12:45
on a series of videos around skills and
12:47
the SDLC for a modern agentic developer.
