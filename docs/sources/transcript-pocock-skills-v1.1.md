0:00  Hello friends. First video in a while

0:01  and that is because I've been working on

0:04  version 1.1 of my skills repo. It has an

0:07  astonishing amount of stuff in there.

0:09  There is an entire new approach to

0:11  grilling which probably deserves its own

0:13  video, but I'll try and squeeze it in

0:14  here. There is a bunch of new changes to

0:18  existing skills, including a rename of

0:20  two main flow skills. There is just

0:22  really way too much for me to summarize

0:24  in this intro, so you're just going to

0:26  have to watch the video to find out. We

0:27  can see the PR is literally ready to

0:29  merge now. So, why not? Let's actually

0:32  freaking merge this thing. And just like

0:33  that, we have our version 1.1 ready to

0:37  go. Let's start with the two that are

0:38  probably going to be most annoying for

0:40  you and the most like why did he do

0:42  this? And there is a very specific

0:45  reason that I did it, which is that two

0:47  skills have been renamed. For instance,

0:50  two PRD has now been renamed to two

0:53  spec. And if we go up one level, then we

0:55  go to two uh issues has been renamed to

0:59  two tickets. The reason I've done this

1:01  is that this has just been bugging me

1:03  for a long time. The thing that we were

1:05  creating into PRD wasn't actually a PRD.

1:08  It was a spec. A product requirements

1:11  document kind of describes more things

1:13  about the actual product itself, whereas

1:16  we were allowing things to leak into the

1:19  PRD that weren't necessarily PRDs. So

1:22  for a long time I've wanted to rename it

1:23  to to spec because that's what we were

1:25  creating. We were just creating a

1:27  specification. Specification is a much

1:29  broader term that actually entails what

1:32  we were building. A specification for a

1:34  thing we want to build. That can be

1:36  technical. It can be non-technical and

1:38  it can blend the two. It doesn't really

1:39  matter. When it came to two issues, two

1:41  issues always felt like it was biased

1:42  towards GitHub and linear that use

1:44  issues. But really we want this to be

1:47  tickets. you have a spec and then

1:49  underneath the spec you have the tickets

1:51  that are the journey that you uh take to

1:54  actually enact the spec and create it.

1:56  This has been annoying me for a long

1:57  time and finally it no longer annoys me.

1:59  It brings me joy. Now one irritating

2:01  thing about this rename is that you will

2:03  need to probably delete those skills and

2:05  read them. This means you'll need to run

2:07  npx skills add mapco skills. I'm pretty

2:10  sure that this skills installer won't

2:12  pick up the rename so it won't try to

2:14  update to prd to turn it into tosp spec.

2:17  You get what I mean? And so running this

2:18  command is the safest way to grab all of

2:21  these new skills cuz you get to just

2:22  pick and choose which ones you want. And

2:24  once you've done that, you should

2:25  probably go through a pass through your

2:27  skills folder and just check that uh no

2:29  bad ones are still in there. So you want

2:31  to make sure that you're intentionally

2:33  grabbing all the right skills. The next

2:35  change is that I've fixed a couple of

2:37  bugs that people were having with grill

2:39  me and grill with dogs. Both of them

2:41  rely on this kind of central reference

2:43  grilling skill that kind of show shows

2:45  the LLM how to grill a person. I've

2:48  sharpened up this line here saying

2:50  asking multiple questions at once is

2:51  bewildering even with this d direction

2:54  to ask questions one at a time. It was

2:57  still occasionally just going have

2:59  multiple questions at once. So I've told

3:02  it why we don't want uh multiple

3:04  questions at once. We've also added a

3:06  confirmation gate on the end. do not

3:07  enact the plan until I confirm we've

3:09  reached a shared understanding. Lots of

3:11  people on different models were

3:12  reporting that the grilling session

3:14  would just end and then it would just go

3:16  straight into implementation. So this is

3:18  just an extra little gate there.

3:19  Finally, on some situations, it would

3:22  just grill itself, which is very very

3:25  odd. Not something I've noticed or seen

3:27  in my personal thing, but I I can only

3:29  get a small subset of how these skills

3:31  are actually used. So I've basically

3:34  tried to use a couple of leading words

3:36  to indicate the difference between facts

3:38  and decisions. So sometimes it was using

3:40  the previous phrasing here by just

3:42  exploring the codebase and grilling

3:44  itself. This was especially happening

3:45  with fable actually. And so I've decided

3:48  to make a distinction between facts. So

3:51  facts that are things you find yourself

3:53  by exploring the codebase and decisions.

3:56  So decisions are needed to be made by

3:58  the user. So, just a couple of

3:59  sentences, added a couple of things

4:01  changed around, and this has made it a

4:02  lot more consistent. Definitely getting

4:04  a lot fewer complaints about those weird

4:06  issues happening. The next thing to say

4:07  is that I've added a couple of skills

4:09  that really just take the process that

4:12  was primarily a planning process, didn't

4:15  really hold your hand into

4:16  implementation and turn it into a proper

4:19  software development life cycle. So,

4:20  many folks ask me, what is the flow?

4:22  What is the main flow you're supposed to

4:24  use with the skills? And first of all, I

4:27  mean, this is it. We have number one,

4:29  you're supposed to instead of using plan

4:31  mode, you get an agent to grill you and

4:33  it uses these couple of docs to add a

4:36  glossery to kind of understand you

4:38  better as you go along and also add

4:40  architectural decision records so you

4:42  can capture the non-obvious stuff. The

4:44  stuff that goes in the grill for docs

4:45  then goes into a spec as we saw before.

4:49  That spec kind of defines the

4:50  destination where you're going. Then you

4:54  turn that spec into individual tickets

4:56  so you can spread the development of it

4:58  out over multiple agent sessions. That's

5:00  the purpose of to tickets. You then

5:02  implement each one of those tickets with

5:04  a implement skill. And the implement

5:06  skill is very very simple. It just looks

5:09  like this. Implement the work described

5:11  by the user in the spec or tickets. Use

5:13  TDD where possible at pre-agreed seams.

5:16  That's a nice one. And run type checking

5:18  regularly. Single test files regularly.

5:20  Full test sweep once at the end. Once

5:22  done, use code review to review the work

5:24  and then commit your work to the current

5:26  branch. I almost didn't make a skill for

5:28  this because it's really simple, right?

5:30  It's just mostly relying on the agents

5:32  prior on its, you know, on the harness

5:34  kind of teaching it what to do. And I

5:37  didn't honestly think we needed a skill

5:39  here. But folks kept asking me what's

5:41  the flow? What's the flow here? And so I

5:43  figured just an implement skill, make it

5:44  nice and simple, right? At each stage of

5:46  the process, call this skill. So that

5:48  means implement earns its place here

5:50  because you know okay once we got two

5:52  tickets then we just got to implement

5:54  each ticket in a separate coding

5:56  session. Implement then itself calls

5:58  code review and code review I graduated

6:00  this out of in progress on version one.

6:03  So it's been around for a little bit but

6:06  I have made some updates to it in this

6:07  version two. The theory of the code

6:09  review skill is that it reviews code on

6:11  two axes. So it does a sub agent for

6:14  each one of these. The first one is the

6:16  standards axis. Does the code conform to

6:18  this repo's documented coding standards?

6:21  So, if you've got a coding standards.md

6:24  file somewhere in your repo, then it

6:26  will read that and check against those.

6:28  I generally think that coding standards

6:30  belong outside of your agents.md file.

6:33  They're supposed to be somewhere

6:34  separate and the code review point is

6:36  where they're most useful. And then once

6:39  you've done the standards, you then go

6:40  on to the spec. Does the code faithfully

6:42  implement the originating issue or PRD

6:45  or spec? They both run as parallel sub

6:47  agents and it does a process here where

6:50  it walks through each part. Now the

6:52  thing that's cool and new about this

6:53  skill is that I've been reading Martin

6:55  Fowler's Refactoring again. And what I

6:58  decided to do is Martin Fowler names a

7:00  bunch of different smells that the agent

7:03  can identify in bad code. Refactoring is

7:06  such an old book, such a well-sighted

7:08  book that these uh kind of smells are

7:11  deep in the agent's prior. And so all

7:13  you need to do is kind of invoke the

7:14  idea of okay mysterious name or

7:16  duplicated code or feature envy data

7:18  clumps primitive obsession repeated

7:19  switches divergent change speculative

7:21  generality message chains you see what I

7:24  mean like these are all deep in the

7:26  agent's kind of knowledge base and all

7:27  we got to do is just really describe

7:29  them in a sentence and what I found is

7:32  that leads the word or leads the agent

7:34  to repeat that word back to you and say

7:36  yes I found some message chains I need

7:39  to remove them I found a middleman

7:41  situation I need to uh fix that. So, I

7:43  tested this for a couple of weeks and it

7:44  was outrageously useful. It was really,

7:47  really nice at improving the quality of

7:48  my code and it's really cheap to add

7:51  here. Just kind of like 10 lines. But,

7:53  let's go and talk about the one that I'm

7:54  really really excited about, which is a

7:57  whole new change to the way that we kick

8:00  off and shape specs. So, the pre-spec

8:04  bit. In other words, it goes here where

8:06  it may in some situations replace Grill

8:09  with Docs and it's called Wayfinder. I

8:12  will make an entire post, entire video

8:14  about WFinder, but uh suffice to say is

8:16  that I would love for you in situations

8:19  where you're thinking about using Grill

8:21  with Docs instead to default to Wfinder

8:24  instead. What Wayfinder does is it's

8:26  designed for situations where you have a

8:28  ton of stuff that you want to plan but

8:31  and too big for one agent session. In

8:33  other words, you're going to blow out of

8:35  the smart zone of the agent or you might

8:36  even blow out of the context window of

8:38  the agent. You need to split it into

8:40  multiple parts in order to figure out

8:42  where you're going. A loose idea has

8:44  arrived, too big for one agent session

8:45  and wrapped in fog. The way from here to

8:47  the destination isn't visible yet. This

8:49  skill charts the way as a shared map on

8:52  the repo's issue tracker, then works its

8:54  tickets one at a time until the route is

8:56  clear. These maps are saved in GitHub

8:58  issues. For instance, this is one on the

9:00  Sand Castle repo where we're doing a

9:02  spike to think about maybe pulling in

9:04  the AI SDK as a dependency. A big big

9:07  change. And so you can see there are no

9:09  decisions that have um been made so far

9:12  and all of the decisions that need to be

9:14  made are saved in sub issues and these

9:16  sub issues have blocking relationships.

9:19  So we can see that no decision can be

9:21  made here before we make this key

9:24  decision at the start. Each one of these

9:26  decisions is scoped to be the size of an

9:29  agent session. And we can see that

9:30  they're labeled as different types here.

9:32  So for instance, this one is labeled as

9:34  a research task. So, this is really an

9:36  AFK task for the agent to go off, do

9:39  some research, and then come back. This

9:41  one, I think, is a research as well.

9:43  This one is a research task, and this

9:45  one is a grilling task. So, this one

9:47  needs a grilling session to be done

9:49  here. I think these are all grillers. We

9:52  can see these defined in the ticket

9:53  types down here. So, we have research,

9:55  we have grilling, we also have prototype

9:58  as well. So this is something I've been

10:00  really advocating for recently is doing

10:03  more prototyping before you get to a

10:05  spec. The idea is you raise the fidelity

10:07  of the discussion by making a cheap

10:09  rough concrete artifact to react to an

10:11  outline rough take UI logic code via the

10:14  prototype skill. We'll get to that in a

10:15  minute. Links to the prototype as an

10:17  asset. And it says use when how should

10:19  it look or how should it behave is a key

10:22  question. And this is essential for

10:24  almost anything that touches front-end

10:26  code. So I would definitely be

10:28  recommending using Wfinder for anything

10:30  that touches the front end. The final

10:31  one here is just tasks. So config that

10:34  needs to be set up um provisioning

10:36  access, you know, moving data into the

10:38  shape, you know, all the sort of boring

10:40  stuff that doesn't need a grilling

10:42  decision and can't really be automated

10:44  by AI. What you end up with is after all

10:47  of these tickets are closed, all of that

10:49  information gets saved onto the map with

10:51  the original tickets as kind of primary

10:53  sources for what was captured. And you

10:55  can then take this map and just turn it

10:58  into a spec in the regular way. What

11:00  I've found that instead of having the

11:01  kind of anxiety of managing my session

11:03  with Grill with Docs, having to hand

11:05  off, worry about the smart zone, with

11:07  Wayfinder, it's kind of all managed for

11:09  me, I just get to close a session, open

11:12  up the next Wayfinder ticket. It's all

11:14  saved in GitHub, so it's collaborative.

11:16  You can share it across your team. And

11:18  once the map is done, once it's

11:19  complete, you just go to to spec and

11:21  you're good to go. To support the

11:22  wayfinder skill, we have a new research

11:24  skill which is very small, very handy

11:27  for when you just need to do a research

11:29  session or it kind of influences the

11:32  model in researching in the right way as

11:33  well or at least the way that I like.

11:35  Spins up a background agent to do the

11:37  research so you keep working while it

11:38  reads. Investigate the question against

11:40  primary sources. Write the findings to a

11:41  simple markdown file and save it where

11:43  the repo already keeps such notes match

11:45  the existing convention. So this is

11:47  useful too if you need to do any

11:48  research. you can just invoke the

11:50  research skill and you're good to go.

11:51  The next one, of course, is the

11:53  prototype, which I've kind of shown off

11:55  a little bit before. I don't think I've

11:57  done a full video on it. This is now

11:59  model invoked so that Wayfinder can

12:01  invoke itself and it essentially gives

12:03  you a choice between logic or state. So,

12:06  it's either a logic prototype or a UI

12:10  prototype, and they react quite

12:12  differently. The final change is

12:13  something that people have been asking

12:14  for for a while and I finally decided to

12:16  pull the trigger on it which is before

12:18  in my TDD skill it would recommend a set

12:21  of steps for you to follow and that was

12:23  a little bit awkward sometimes. the

12:25  steps were like it would confirm what

12:27  tests it wanted to write with you and

12:30  then you would you know walk it through

12:32  walk it through and it didn't fit with

12:34  most people's uh idea of how TDD should

12:38  work which is you should be able to pass

12:40  an AFK agent the TDD skill and it should

12:43  just work and so this TDD skill is now

12:45  reference material only so it doesn't

12:48  specify any particular steps apart from

12:50  just the order in which you should write

12:52  tests in so to do red green refactor so

12:55  It just says red before green one slice

12:56  at a time. And it also splits away uh

12:59  refactoring as as not part of the loop.

13:02  So it's no longer a red green refactor

13:04  loop. It's more just red green. I tend

13:07  to think that putting the refactoring in

13:10  the code review part is a lot more

13:13  productive because then you don't

13:14  overload the implementation. So that is

13:17  all of the changes that have come in on

13:19  the skills. It is a lot of changes. And

13:22  if you're nervous about missing any of

13:24  the updates, then I recommend that you

13:25  clear out all of your skills and do npx

13:28  skills update and grab all of the new

13:30  ones. If you've made updates to your

13:32  skills in the meantime, then you can

13:33  just point your clanker at my repo and

13:35  just say pull down all of the good new

13:37  stuff, especially pointing at the

13:38  release notes. The thing I think this

13:40  release will be remembered for is to

13:42  spec and to tickets changing because

13:43  that is just a little bit of friction,

13:45  but I think good friction because it

13:46  names it properly and I hope to be the

13:49  start of you getting obsessed with

13:51  Wfinder. I'm using Wayfinder for

13:52  literally everything, even non-coding

13:55  stuff. I've actually been planning my

13:56  next course with Wfinder and it's

13:58  really, really good. And in fact, why

14:00  don't I just show you that course now?

14:02  This is the AI coding crash course. This

14:05  is going to be different from the

14:06  cohorts that I usually run. It's going

14:08  to be much much cheaper and it's going

14:10  to be self-paced so you can purchase it

14:12  anytime. You get help from the Discord

14:14  kind of in the usual way, but it's not

14:16  going to be gated like a normal cohort.

14:18  It is going to be the perfect intro for

14:21  anyone who's looking to get into AI

14:23  coding whether you are a developer or

14:25  whether you are not a developer. So for

14:27  senior engineers, it's going to be a

14:29  conversion course. For folks who are new

14:31  to development, it's going to be the way

14:33  that you can actually get productive

14:34  using these crazy new tools. I've not

14:36  announced a price yet. I am going to

14:38  just be adding signups in here and it

14:40  will be available once I finish filming

14:42  it. Maybe in about uh August time I

14:45  think. But folks, thank you so much for

14:47  watching. It's always a pleasure sharing

14:48  these skills updates with you. It is

14:50  really cool to see the usage just

14:52  absolutely grow and grow. Everyone tells

14:54  me I shouldn't show the star count, but

14:56  it's up to like 160k stars now. There

14:59  are 7 million downloads on Skills.sh. It

15:01  is just bonkers. So, thank you so much

15:03  for enjoying the skills. I hope they are

15:06  helping you ship more and ship more

15:08  productively