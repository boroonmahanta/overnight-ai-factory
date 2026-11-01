0:00  Hello folks, version 1.3 of my skills

0:03  repo is out and it brings three very

0:06  important skills that have become

0:07  central to my workflow. Today I'm going

0:09  to show you about implement spec. I'm

0:11  going to show you about PR and I'm going

0:13  to show you about retro. And retro I

0:16  think is the one that I've just seen

0:19  absolutely go nuts on socials. People

0:21  going crazy for this skill and it has

0:24  felt incredibly powerful to me too. And

0:26  the first place I want to start is the

0:28  implement spec skill. The main flow of

0:30  my approach for landing huge chunks of

0:33  work at once is essentially two

0:35  different entities. You have a spec and

0:38  then you have the tickets that implement

0:40  that spec. The spec kind of acts like

0:42  the place where you're going and then

0:44  the tickets break that destination down

0:47  into a set of sessions that you can then

0:50  run in a single coding agent. If you try

0:52  to implement the spec all in one coding

0:54  agent, you would go into the dumb zone

0:56  of that coding agent, you might end up

0:58  hitting auto compact. And you know,

1:00  while that works sometimes, and it is

1:02  getting better, I still think that

1:04  breaking things down into individual

1:06  tickets is just a lot cleaner. Now, the

1:08  way that you orchestrate those tickets,

1:09  the way that you give them each to one

1:12  coding agent has always been a little

1:13  bit confusing for users. And I've kind

1:16  of been sort of going back and forth

1:18  over the way that I recommend you do

1:20  this. The most annoying and manual way

1:23  to do this is managing it yourself where

1:25  you the user say okay uh agent we are

1:28  going to implement our first ticket. You

1:30  wait for it to be complete. You clear

1:32  the context and then you say okay

1:34  implement ticket two. You wait. You

1:36  clear the context. You say implement

1:38  ticket three. You're kind of acting like

1:40  a for loop there. It's not really

1:42  workable. So that is what I would

1:44  describe as the manual loop there which

1:46  is not much fun. But you can change that

1:49  by having a deterministic loop where you

1:51  have a script that reach uh reads each

1:53  ticket and then runs implements on it

1:55  itself. This is how I recommend that

1:57  most people do this because once you've

1:58  set up your deterministic loop, it's

2:00  going to run the same way every time.

2:02  It's very reliable and it's cheap,

2:05  right? Because you're not using an agent

2:06  or you're not using a human to run that

2:09  loop. You just essentially get a script

2:11  to do it for you. But setting this up is

2:13  quite complicated and requires a lot of

2:16  patience as you sort of refine your loop

2:18  and get it better and better. And so I

2:20  see this as out of range for beginners.

2:22  And so I wanted some way of allowing

2:26  beginners to see not have to manually

2:29  loop it themselves. And so I decided,

2:31  okay, why don't we try a middle ground

2:34  where we have sub agents go through and

2:37  implement the loop. In other words, an

2:38  agent does the babysitting instead of a

2:41  human. This means that all of the

2:42  tickets will be implemented by sub

2:44  agents. And this has recently gotten

2:47  possible because sub aents can

2:49  themselves spawn sub aents. So before

2:52  sub agents were kind of a little bit

2:54  nerfed whereas now they're actually as

2:56  powerful as orchestrator agents. And so

2:58  this is what implement spec does is it

3:01  the agent sits there looking at all of

3:03  the tickets orchestrating them and then

3:05  implements them in sub aents. This is I

3:08  would say worse than doing a

3:10  deterministic loop because the

3:11  deterministic loop again it's

3:12  deterministic. It works the same way

3:14  every time. But implement spec is a good

3:16  way to get started with AFK workflows

3:19  away from keyboard workflows where you

3:21  step away and it implements the entire

3:23  spec. Before you use any skill, you

3:25  should read the entire skill. And it's

3:27  not particularly long here. There are

3:30  nine steps in its process and it's got a

3:32  little bit of reference material just at

3:33  the top. One crucial thing is it goes

3:35  for parallelization where it can. And so

3:37  this says the tickets are not a list of

3:39  steps. They're a task graph with

3:41  blocking relationships between them.

3:43  That means there's always a frontier of

3:44  tickets that are ready to be grabbed. If

3:46  we take a look at the steps, we can see

3:47  it reads the spec and tickets. It does a

3:50  little bit of exploration in its own sub

3:52  agent. It creates an integration branch

3:55  and then it goes and uses implement sub

3:57  aents to implement each ticket using TDD

4:00  and using work trees too. Once that's

4:02  done, it merges its work to the

4:04  integration branch with a sub aent and

4:07  then pings off more implement sub aent

4:09  until all the work is done. And once it

4:12  the work is done, it goes and calls code

4:14  review on the integration branch. Then

4:16  it cleans up all of its work and makes

4:18  the PR ready for review. So you get a

4:20  single PR off this huge great big spec.

4:23  I have been reaching for this a lot more

4:25  than I thought I would, especially on

4:28  systems where you haven't set up these

4:29  deterministic scripts yet, where you

4:31  don't have your like software factory

4:33  dialed in. I suppose implement spec has

4:36  been really really useful. It's been in

4:37  in progress for a while now, but I

4:39  thought now's the moment. Let's graduate

4:41  this so people can use it and fiddle

4:43  around with it and build their own

4:44  version of this, too. This is a basic

4:46  version of how you might implement your

4:48  own spec. You could do something totally

4:50  different to this. You could use stacked

4:52  PRs. You could do all sorts of stuff.

4:54  And in fact, talking of PRs, one of uh

4:56  my most used recent skills has to be the

4:59  PR skill. So, PR skill.md. I've been a

5:02  huge fan of Dex Hies for a while now. I

5:04  recently got to meet up with him in

5:06  person and he has this gorgeous skill

5:08  called Show Me. What show me does is it

5:10  helps the user understand the current

5:12  topic visually with concise diagrams and

5:15  it uses all of this like uh really nice

5:18  pseudo code. This looks a little bit

5:20  garbage, but actually when you see it in

5:22  the context of a PR, it really makes the

5:25  PR a lot easier to read and review. PRs

5:28  are still the main bottleneck for work

5:30  getting to Maine. And my goal with this

5:33  PR skill, kind of inspired by Show Me,

5:37  is to make human review as easy as

5:40  possible. And in the skill, we provide

5:41  essentially a template for writing a PR

5:44  body. That's all the skill does. We

5:46  first start with a summary based on the

5:48  kind of show me template which we

5:50  include in the skill and then we ask for

5:53  evidence. So before and after. This

5:55  evidence is an essential part of

5:57  learning to trust your agent, learning

6:00  to trust your agents outputs. and

6:01  actually prompting it to provide

6:03  evidence often means it runs an extra

6:05  test or it takes an extra screenshot if

6:07  it has that ability and it provides you

6:10  runtime information on that it's actual

6:14  change is doing what it thinks it's

6:15  doing without asking for hard evidence

6:17  it's very easy for agents to say yeah

6:19  that probably works cuz I've read the

6:20  code but no verification is something

6:22  I'm beginning to be really obsessed with

6:25  especially after my recent interview

6:26  with Lauren and then the third heading

6:28  here is merge danger so how dangerous Is

6:31  this PR going to be to merge? One

6:33  metaphor I've really like here is, is

6:35  this a one-way door or is this a two-way

6:38  door? A two-way door is a door that you

6:40  can walk back through. In other words,

6:41  we can easily revert this PR. But a

6:44  one-way door is a, you know, a PR that's

6:46  going to do something out in the world.

6:49  It's going to delete some data or it's

6:51  going to be expensive in some way to

6:53  roll back. And then finally, you have

6:54  blast radius here. So the potential

6:56  ramifications of the changes. So, if you

6:59  have a very small blast radius on a

7:01  two-way door, then, you know, you really

7:03  don't need to like review that PR very

7:05  hard. And so, having this at the bottom,

7:07  probably the, you know, first or second

7:09  thing the person is going to see is

7:11  essential. So, for instance, here's one

7:13  of the PRs in my repo that has been

7:15  provided by the PR skill. This is

7:16  essentially merging two algorithms that

7:19  were basically the same. And we can see

7:21  the files deleted and the files added in

7:23  the right context. We understand the

7:25  functions, the sort of the call stack

7:27  that's being structured here, but

7:28  crucially, we have the evidence. We have

7:30  a before and after on a real entity. So,

7:33  there's no intro in this one, but

7:35  afterwards, it adds the intro, which is

7:37  kind of the behavior that we want here.

7:39  And finally, we can see that the merge

7:40  danger is two-way. It's just a pure

7:42  refactor plus one deliberate behavior

7:44  change, and the blast radius is small.

7:46  So, this PR skill is just become

7:48  absolutely indispensable to my flow. It

7:50  is also one of the most consistently

7:52  invoked model invoke skills that I've

7:54  seen. The you you the user don't have to

7:57  worry about it at all. It seems to just

7:59  invoke it every single time, at least on

8:01  Opus 5.5. So you should just be able to

8:03  download it and just see your PR bodies

8:05  get better. And of course, if you

8:07  already have a PR body skill, then why

8:09  not just steal what you can from this?

8:11  Now, before we talk about the retro

8:12  skill, we should mention that there has

8:14  been a big change in how my especially

8:17  grill with docs function. So let's take

8:19  a look at domain modeling here and

8:21  domain modeling skill now instead of

8:25  writing to context.md writes to

8:27  glossery.mmd. The inspiration for this

8:29  skill came from DDD came from Eric

8:32  Evans's book domain driven design. And

8:35  [snorts] for that I was essentially

8:37  using a file name based on the concept

8:40  of bounded context from DDD. And so this

8:43  used to be context.md like this. But now

8:47  I've sort of moved away from the DDD

8:50  style flow. I mean, I still use DDD in

8:53  all but name, but I wanted a slightly

8:56  less overloaded term here. Context.md

8:59  just felt way too vague. It didn't sort

9:02  of trigger the agent to pull it in at

9:03  the right moment. And for users, it was

9:06  pretty confusing. I also ended up

9:07  reducing the amount of stuff in glossery

9:10  or in context.md until it was literally

9:12  just a glossery. So there really is no

9:14  point anymore. glossery.mmd is now what

9:16  we're going this is also updated

9:17  everywhere and so loads of my skills

9:20  rely on seeing a glossery.mmd in order

9:23  to behave properly in order to use the

9:24  domain language at all points and so you

9:27  will need to definitely update this.

9:29  There's no other behavior changes about

9:30  the skill. It's really literally just a

9:32  file name change and I think that this

9:35  is one that folks have been wanting for

9:36  a while. So I'm glad to ship it. But now

9:38  let's take a look at the retro skill and

9:40  let's actually do it by running it. What

9:43  I noticed with my skill set is that I

9:46  impose a lot I ask a lot of you the

9:49  user. And what I was kind of asking of

9:52  you is you were responsible for overtime

9:58  making changes to the repo that would

9:59  improve it. In other words, I was asking

10:01  you to manage your agents.mmd to manage

10:04  your skills, to make sure that your repo

10:06  was token efficient, to make sure that

10:08  your environment was good and safe for

10:10  the agent to write code in, that you had

10:12  good lint rules, that you had good

10:13  navigation. And I realized that I

10:15  personally was doing a lot of stuff to

10:17  my repos to my agents in order to make

10:20  them easier for me to work with to make

10:22  them more performant. And so I realized,

10:24  why don't I bundle that up into a skill?

10:27  And this is what retro does. It is short

10:29  for retrospective. You run it on a

10:32  coding agent session, either the current

10:34  one or, you know, 10 that I've currently

10:37  got or let's say the previous one, and

10:39  it will suggest improvements for next

10:41  time. The cool thing about actually

10:42  reading real sessions here is that it's

10:45  able to look at what happened with the

10:48  agent. It's able to see the

10:50  inefficiencies that maybe the agent

10:51  actually hides from. I really like this

10:53  post from Andre Retro by Mogers. Game

10:55  changer. My agents are bumping into all

10:57  kinds of problems. that went undetected.

11:00  But due to persistence, the features

11:02  still got built one way or another. In

11:03  other words, the agent doesn't complain,

11:05  I think, as much as it should, and

11:08  doesn't try to fix its own mistakes. You

11:11  kind of need to get another agent to

11:13  look back on those sessions and see

11:14  where it went wrong and see how to help.

11:16  And so, this is what our agent has found

11:19  here. The agent ran an irreversible

11:20  public action before you picked a fix.

11:23  The agent found why the 1.3.0 release

11:25  was missing and then it ran a release

11:27  without actually asking. This is why, by

11:29  the way, when you actually look at the

11:30  releases, you'll see there's no 1.3.0

11:33  release, only a 1.3.1 release. You know,

11:35  Claude kind of screwed this up. I don't

11:36  honestly care that much about it, so I

11:39  don't mind this one in my context. We

11:41  can see that this particular repo in has

11:43  no actual guard rail. So, there is a

11:45  PNPM check script, but nothing actually

11:47  runs it. So, it's suggesting adding a CI

11:50  pipeline here. In here, we can see

11:52  there's context loss happening between

11:54  compactions in long sessions. So, I use

11:57  animatics to kind of create my videos or

12:00  early drafts of them now. And it's

12:02  saying that there's some loss when you

12:04  compact. And so, it's saying move some

12:06  of the repeated instructions into an

12:08  animatic skill. This is definitely a

12:10  really good one, and I'm definitely

12:12  going to implement that for sure. Oh,

12:13  look at this one. A custom CLI that I've

12:15  created for my course video manager

12:17  wastess tokens. So, Retro looks at token

12:20  inefficiency too. Wiki, which is another

12:22  custom CLI, is not on path locally and

12:24  Wiki AI hero has gaps. So, Retro is

12:27  merciless. It will look at your actual

12:30  sessions and see what is going on and it

12:32  will pretty much always find ways to

12:34  improve. Now, what I'd say with Retro is

12:36  you want to use your human judgment when

12:39  you look at these. I know, for instance,

12:41  the thing that it thinks is most serious

12:43  is actually not that bad. It's just a

12:46  release. I can always create and cut new

12:48  releases. And so the way retro works is

12:50  it's designed to be human in the loop.

12:52  It's not designed to just keep creating

12:54  these fixes random. Pretty much everyone

12:56  when I show them this, they go, "Ooh,

12:58  I'd love to automate this." No, you

12:59  don't want to automate this. Automating

13:02  this means that the agent will get

13:03  itself into a loop where it continually

13:06  finds false positives. It continually

13:08  tries to fix things and you'll end up in

13:10  this weird trajectory where it just

13:12  takes the repo and your agent into a

13:14  place it shouldn't really go. So, I

13:16  recommend you run retro on a sampling of

13:19  your agent sessions. Every time you've

13:21  got a free moment and you realize, "Oh,

13:23  I haven't run retro in a while." Just

13:25  try getting it to run through your most

13:27  recent sessions. Maybe a session that

13:29  has gone wrong, let's say, or you feel

13:31  the agent has done something weird, and

13:33  retro will usually find a fix. We can

13:35  see that inside the steps in the retro

13:37  skill, it has several categories for

13:39  improvements that it looks for. How easy

13:41  is your codebase to navigate? Are there

13:44  automated checks that we could add?

13:46  Could we add coding standards for the

13:47  automated reviewer to enforce? How

13:50  healthy is the global agents.mmd? Is the

13:52  tool economy any good? Are there any

13:54  noops in the instructions in steering

13:56  files? Does the agent have access to all

13:58  the information it needs? Overall, I've

14:00  seen my token efficiency and just the

14:02  quality of work that I've been able to

14:04  produce massively increase by running

14:06  retro regularly. And if you want to see

14:08  the quality of your work increase too,

14:10  then I recommend you take my AI coding

14:12  crash course which is on aihero.dev. I'm

14:14  updating this today with a new lesson

14:16  focusing on implement spec. And if you

14:17  want to take control of your coding

14:19  agent and utilize my skills better, then

14:21  this is the place. But folks, thank you

14:23  so much for following along. Hopefully

14:24  you enjoy Skills V1.3. Enjoy seeing the

14:28  uncomfortable truth of how bad your