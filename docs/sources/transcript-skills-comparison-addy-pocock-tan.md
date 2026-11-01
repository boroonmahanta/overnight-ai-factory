Source: YouTube video https://www.youtube.com/watch?v=sU9MW8Ycq2M. Boroon's description: this video compares the three people we have been reviewing, Matt Pocock, Lauren Tan and the latest Addy Osmani. GitHub links: Addy Osmani https://github.com/addyosmani/agent-skills ; Lauren Tan (Poteto) https://github.com/cursor/plugins/tree/main/pstack ; Matt Pocock https://github.com/mattpocock/skills . Boroon's intent for this document: compare the three, take the best of each, take the "T-Shirt Size" approach to building and developing, and use the relevant skills and tools from the three repos. Transcript pasted into the chat by Boroon on 1 November 2026 as "Transcript 2". Saved verbatim as pasted, including chapter headings.

---

Intro
0:00
So Adas Manny, he's probably one of the
0:02
most respected engineers at Google for
0:05
well over a decade. And he's recently
0:06
just moved to Anthropic, the maker of
0:08
Claw Code, and he's just gone and open
0:10
sourced all his agent skills. So 100,000
0:13
stars later, it's probably one of the
0:15
most popular AI repos on GitHub right
0:17
now. So if you've been following the
0:19
channel at all, you'll know I've already
0:21
broken down Pstack from Lauren Tan at
0:23
Cursor, and then also Matt PCO's skills.
0:26
So Addi is the third of the big three.
0:28
Now that we've got all three, you can
0:29
see that they're solving different
0:31
problems. By the end of this video,
0:32
you'll know what ADI is doing, when to
0:34
reach for each pack, and why I think you
0:37
don't need to run all of these across
0:38
all of your projects. They can be a bit
0:40
of overkill sometimes. I'm Rob. This is
0:42
Switch Dimension, and let's start with
0:43
how Addy thinks about his skill set. So,
Who is Addy Osmani
0:46
quick context. If you don't know who
0:47
Addi is, he's a bit of a legend in the
0:49
JavaScript world. He wrote Learning
0:51
JavaScript Design Patterns. He led the
0:52
Chrome developer experience and web
0:54
performance work at Google. If you've
0:56
ever run Lighthouse or read about Core
0:58
Web Vitals, you've probably been
1:00
affected by his work at some stage. So,
1:02
I think that's really relevant because
1:03
when somebody like Addi writes down this
1:06
is how you want an agent to engineer
1:08
software, you want to pay attention.
1:10
What you're really getting is a seasoned
1:12
engineer's brain compressed into
1:14
markdown. And that's what I love about
1:16
skills. Before we read tons of O'Reilly
1:18
books on best practices, now we're
1:20
basically studying and examining skills
1:22
from the top performers. So, here's the
1:24
big idea. Addi's approach is a life
1:26
cycle, six stages. Define, plan, build,
The six-stage lifecycle
1:30
verify, review, ship, and each stage has
1:33
a slash command to go with it. If you've
1:35
been watching my videos for the last 2
1:36
years, or you've done any kind of specd
1:38
driven development with BMAD or
1:40
superpowers, this will feel very
1:42
familiar, and that's kind of the point.
1:44
Math skills have their own vocabulary,
1:45
grilling and wayfinder and fog of war.
1:48
Pstack has potato mode and arenas. Addis
1:51
is the most traditional to the software
1:53
development life cycle. You don't have
1:54
to learn a metaphor. It's the software
1:56
development life cycle done properly
1:58
with an agent. So I think of all the
2:00
stacks this can fit in very well with an
2:02
existing development team or in the
2:04
enterprise. So spec writes a proper PRD
2:07
covering objectives, structure, code
2:10
style, testing and boundaries before a
2:13
line of code. Plan breaks that into
2:15
small atomic tasks with acceptance
2:17
criteria and build implements one thin
2:19
vertical slice at a time. You implement
2:21
it, you test it, you verify, you commit
2:24
it, then you test, review, and ship. So
2:25
there's one mode that I really like.
2:27
It's called slashbuild auto. So you
2:29
approve the plan once and then it runs
2:31
every task autonomously after that. It
2:33
removes you kind of having to step in
2:35
between tasks, but it doesn't remove the
2:37
verification, which is important for you
2:39
to look at. So every task is still test
2:42
driven and it's committed on its own and
2:44
then it stops if something fails. So I
2:46
think that's kind of like the right way
2:47
to do autonomy. So slash constraints
2:50
basically is another style of interview
2:51
just to test out what your quality level
2:54
or quality bar is and then it writes
2:56
this to a constraints.mmd file. Then
2:58
there is a /web perf for web
Inside the skills
3:00
performance. It does a performance audit
3:02
which you know given who wrote this at
3:04
Manny the the king of web performance.
3:07
You'd hope this is going to be good. And
3:08
then slashcode simplify is for when the
3:11
code works but nobody really wants to
3:13
touch it and you want to simplify or
3:15
break it down. There's a lot of overlap
3:17
between what Lauren talks about and also
3:19
what Matt PCO talks about in terms of
3:21
similar skills. So there's 25 skills in
3:24
total plus four reviewer personas.
3:26
There's a staff engineer, a test
3:28
engineer, a security auditor, and a web
3:31
performance auditor. Okay, so let's look
3:32
inside the skills. As always on this
3:34
channel, the slash commands aren't the
3:37
interesting part. The skill files are.
3:39
Here's where we really get inside a
3:41
software engineer's brain. So, every
3:43
skill has what Addi would call a
3:45
anti-rationalization table. It's a list
3:47
of the excuses an agent will make to
3:50
skip past a step. We see agents doing
3:52
this all the time. And then you've got
3:54
the rebuttal to why it would skip right
3:56
next to it. So, it'll test for things
3:58
and reasoning traces like this is too
4:00
simple to test or I tested it manly. So,
4:02
if you've worked with agents or you've
4:04
worked with juniors, you've heard all
4:05
these excuses before and writing the
4:07
excuses down in advance is really a
4:09
smart move. Here's a quick tip on
4:10
working with multiple agents. Thanks to
4:12
our friends over at Neon. When you're
4:14
developing new code with agents, you're
4:16
going to want to have multiple different
4:17
feature branches just to be sure that
4:19
you don't impact the main production
4:21
branch. Unfortunately, it gets a bit
4:23
more complicated than that. We have the
4:24
main branch, but we also need a database
4:26
branch and maybe even some storage.
4:28
Otherwise, what you get is a preview
Sponsor
4:30
branch. Maybe it's got a copy of
4:32
Postgres, and that's okay. But then it
4:34
might end up uploading the file to the
4:36
wrong storage and we end up with a
4:38
production break. I've been using Neon
4:40
for years for my database needs just
4:42
because of their superior branching and
4:43
a whole lot of other reasons. But what
4:45
you might not have noticed is now
4:47
they're a full platform database
4:48
storage, functions, o and AI gateway.
4:51
Why is that a beautiful thing you might
4:53
ask? So your agent using the CLI can now
4:55
create a branch of everything it needs
4:57
to be safe. That includes your database,
5:00
your functions, your buckets, your user,
5:02
anything that you need. Each agent gets
5:04
its own copy instantly. Rob Shocks
5:06
viewers can sign up to Neon for free via
5:08
the link in the description down below.
5:10
So this one is really interesting. It's
5:12
called [snorts] doubtdriven development.
5:14
We've heard of domain driven
Pocock vs Addy vs pstack
5:15
development. This is doubt driven
5:17
development. So for any non-trivial
5:19
decision or important decision, it spins
5:21
up a fresh context review. And the one
5:23
job is to doubt the claim. So claim,
5:26
extract, doubt, reconcile, stop. It's
5:30
basically adversarial review during the
5:33
build, not just at the end. As you start
5:35
to read through the rest of the skills,
5:36
you start spotting some old friends and
5:39
paradigms. Hyram's law in the API design
5:42
skill. So, every observable behavior of
5:44
your API will eventually be depended on
5:46
by somebody. And then the Beyonce rule
5:48
in the testing skill. If you liked it,
5:50
you should put a test on it. I'm not
5:52
going to sing this. And Chesterton's
5:54
fence in code simplification. Don't
5:56
delete the fence until you know why it's
5:58
there. Trunkbased development, small
6:00
atomic commits, code as a liability. So
6:04
that's basically Adi Assani's software
6:06
engineering brain turned into agent
6:08
instructions. Honestly, if you never
6:10
install this, just reading through the
6:11
skills is a better software engineering
6:14
course than most. So how does this
6:16
compare to the other two? So Matt PCO's
6:18
skills basically are asking, do we agree
6:21
on what we're building? So do you and
6:23
the agent agree? You're setting up the
6:25
domain. His most popular skill would be
6:27
grill meat. And that's basically where
6:29
the agent interrogates you before it
6:31
writes anything. Then there's the idea
6:32
of a shared language glossery which
6:35
would be ADRs which are decision records
6:37
and then you've got specs and tickets.
6:39
Matt still falls in with the traditional
6:41
SDLC. It's just he is approaching it in
6:44
a different way. A lot of his skills put
6:47
the effort up front before you actually
6:49
begin to code. And he's openly said he's
6:52
anti-framework. He thinks things like
6:54
BMAD specit superpowers take away your
6:56
control. So his skills are deliberately
6:58
small. They're composable and you can
The $87 head-to-head
7:01
use them where you need to and hack them
7:03
yourself. My interpretation of Lauren
7:06
Tan's Pto is really about can you prove
7:08
it works. Lauren deliberately has no
7:10
planning skills. Her line is the best
7:12
spec is the code. All the weight really
7:15
is on the investigation, the
7:16
verification and multimmodal review
7:19
after the fact. The build passed doesn't
7:21
count as evidence. We need to prove that
7:23
out. Addi's skills then are more around
7:26
did we follow the whole process. He's
7:28
the only one of the three that really
7:30
covers the full SDLC life cycle right
7:33
through to continuous integration and
7:34
deployment. Observability, uh,
7:37
deprecation, and shipping. It's probably
7:39
the most teamfriendly and the most
7:41
portable since it installs into
7:43
something like 70 different agents. What
7:45
I've ended up with personally is a mix
7:48
of all of these together. And I don't
7:50
use them all at the same time. I'll use
7:52
different skills at different points.
7:53
I've got light, medium, and heavy
7:55
versions of my skill runtime. So reach
7:57
for poke when the problem is fuzzy, when
You don't need all of this
8:00
you're not sure what you want or you're
8:02
working on a codebase you'll live with
8:03
for years and you really care about the
8:05
design. Grill me is still the single
8:07
best skill I'd install first to do that.
8:10
I'd reach for ADI when you're on a team
8:12
shipping to production and you want a
8:14
predictable process everyone recognize
8:17
or when you want all the quality gates
8:20
without designing them yourself. My own
8:22
skill set falls more in this kind of a
8:24
process because I'm working with teams
8:25
of developers and teaching them how to
8:27
apply agents. Then I reach for Pstack
8:30
when it gets really gnarly. It's a bug
8:32
you can't reproduce. You're looking to
8:34
apply swarms and arenas against a
8:37
problem. There's a migration. You've got
8:38
longunning agents. Maybe it's an
8:40
overnight run and you need to trust them
8:43
when you wake up. And of course, if
8:44
you're running Cursor and you've got
8:45
several models because her skills work
8:48
really well as a plug-in with Cursor.
8:49
And you'll also notice that there's huge
8:51
overlap and they borrow from each other
8:53
constantly. It's not that they're
8:54
actually borrowing from each other. It's
8:55
just that software engineers converge on
8:58
how to build software altogether at the
Build your own skills
9:00
same time. So there is going to be a lot
9:02
of overlap. And again, software
9:04
engineering is opinionated. You just
9:05
pick the best opinion and apply it to
9:07
your own workflow. They're basically
9:09
just three angles here all on the same
9:11
craft. So my actual opinion on all of
9:13
this, you really don't need all of these
9:15
skills on every single project. That is
9:17
a massive overkill. Agents are getting
9:20
super smart now. And one of the best
9:22
things you can do is actually run
9:23
through your agents.mmd file or your
9:26
existing skills and actually start to
9:27
pair them back and prune them because
9:30
you'll be surprised at how powerful the
9:32
models are. I'm thinking that skills now
9:34
are more about this is how I like to
9:37
work as opposed to necessarily teaching
9:39
the agent anything new. In fact, having
9:41
really long skill files and an excess of
9:43
skills is just going to bloat and
Outro
9:45
confuse your context window. So if
9:47
you're just changing a button color, you
9:49
don't need a PRD, a task breakdown, a
9:51
five axis arena review from Pstack, or a
9:55
security auditor. You just need to
9:57
change the button and look at it. So the
9:59
way I think about it is effort level.
10:01
The ceremony should match the stakes of
10:03
what you're working on. So a small
10:05
tweak, just do it and then check it
10:06
yourself. If it's very visual or
10:08
prototype based, just do it yourself.
10:11
Check it quickly, refresh, and move on.
10:12
You're iterating with the agent. If it's
10:14
a small feature, a quick uh grill me or
10:17
discovery session so that you're aligned
10:18
and then some test-driven development.
10:20
If it's a big or fuzzy feature you're
10:23
trying to figure out, then a spec and a
10:25
plan broken down into phases and then
10:27
you verify each one in between. If it's
10:30
production, uh there's security involved
10:32
or anything irreversible, that's when
10:33
you bring out the full review, doubt
10:35
driven development and then all the
10:36
security hardening that comes with it.
10:38
So even Addi says this about his own
10:40
skills. his adoption guide to them is a
10:43
gradual verification first roll out on
10:46
an existing codebase. Don't install 25
10:48
skills and try to run everything. That's
10:51
complete overload. And there is a
10:52
practical cost here, too. Every skill
10:54
you install is something the agent has
10:56
to consider and then you might end up
10:57
autotriggering these skills by accident
10:59
when you don't want them. More skills
11:01
doesn't necessarily mean a smarter
11:03
agent. So, I guess the real lesson here
11:05
is, and I've kind of been saying this
11:07
for a while, learning these skills is
11:09
really learning good software
11:11
development practice. Test-driven
11:12
development, small vertical slices,
11:15
agreeing on requirements before you
11:16
build, writing down why you made a
11:19
decision. You're not deleting the fence
11:20
until you know why it's there. Don't go
11:22
deleting anything until you know
11:24
specifically why it's there, and then
11:26
proving it works against the real thing.
11:27
If you just see green light test, that
11:29
doesn't mean your app works. You need to
11:31
actually test it properly. And none of
11:32
this is new. It's not like any of these
11:34
guys invented this. Matt PCO credits the
11:37
pragmatic programmer and domain driven
11:39
design. Andy is basically Google's
11:41
engineering book. Lauren has years of
11:43
React and meta experience. The skilled
11:46
are just those ideas in a format that an
11:48
agent can follow. So don't treat any of
11:50
these packs as a religion. Treat them as
11:52
kind of like an O'Reilly textbook. You
11:54
can install them, read them, you steal
11:57
what works, and then build your own
11:59
skills on top of them. And that's
12:01
basically encoding how you work. You're
12:03
sharing the best of that with your team
12:05
and they share back. It's your stack and
12:07
it's your own quality bar. This is
12:09
basically your own team or your own
12:11
personal harness. And that's going to be
12:13
bespoke to you and help you move a whole
12:15
lot faster. And every time your agent
12:17
screws something up, don't be a child.
12:18
Don't swear at it. Just go and update
12:20
your skill based on new learnings.
12:22
That's exactly how all of these three
12:24
packs were built. So, if you want to go
12:25
deeper on building your own skills
12:27
library and agent workflows, that's
12:28
exactly what we do
