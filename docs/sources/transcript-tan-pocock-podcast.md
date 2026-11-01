0:00  So, hello folks. I've got another treat for you today. Last time on this kind of

0:05  podcasty thing, I suppose, we had Uncle Bob and we talked about software quality. We talked about agents. We

0:10  talked about lots of cool stuff. Now, we have uh an incredible guest, someone who I'm delighted to welcome on, who's been

0:18  exploding on Twitter recently about software factories, um about increasing

0:24  the quality of your work, about increasing your velocity and climbing the trust ladder with agents so that you

0:30  can ship more and more and more. And it is potato. Welcome. Thank you so much

0:35  for joining. Thanks for having me. Yeah, very excited to be here. Yeah, big fan of yours

0:41  and a huge fan of yours. I [laughter] think people have been talking about this like it's like the meeting of the skill minds, the skill Mount Olympus or

0:49  something because both of us have very popular skill libraries. Um I've not, as I was saying before we started, I've not

0:54  used a ton of yours and like I want to get all of the juice out of your brain so that I can go and use it properly and

1:01  use it better. And I think where I want to start with this is you gave a talk um pretty recently like um about 10 days

1:08  ago and posted on X which went absolutely nuts as about how I shipped 2,500 PRs last month to production got

1:16  about 3 million views or something on X and I watched it and I loved it and I

1:21  recommended it and I kind of want to run this as almost like a Q&A of that talk basically of giving you because it just

1:29  I just had tons of questions about it and I wanted to dive into it. And I think where I want to start is you talk

1:36  about a trust ladder with agents where you as you trust agents more, you can

1:42  get them to do better and better things and or scale them to up to use more and

1:47  more agents. So what is your story of how you climbed the trust ladder and how

1:53  did that work when like you got SpaceX and started climbing more and more?

1:58  So I think this the the journey sort of began even before I joined cursor uh which is now SpaceX AI. Uh [snorts] so

2:06  the story is um after Meta so I I used to work at Meta

2:12  on the React team. [snorts] Uh I took a month off uh because I was feeling kind of burnt out and of course when what

2:19  what do you do when you're burnt out? You go and start a new side project. Um and so I started a side project. you

2:24  know, I was uh of course using AI to to write code. Uh [snorts] but then I started to realize uh you know, I was

2:31  spending like so many hours just micromanaging one agent, right? And you

2:36  know, at the time, this was back in February, maybe February, early February or January, you know, people were really

2:43  obsessed with this idea of like orchestration. This was like, you know, before, you know, things like cursor, you know, like the agents window was had

2:50  become popular. So people were still in like like 2 land you know in their terminal and they were all talking about

2:56  okay here you know I built a custom orchestrator right and so of course I had I was a bit nerd sniped by that

3:03  [snorts] and you know as I was building my toy project uh I got nerd sniped by oh how do I make my AI coding setup more

3:10  efficient and so you know I I kind of started the journey there where I just

3:16  you know took a step back and realized you know I was spending all this time micromanaging a single agent you know I

3:23  was [snorts] creating skills and I was like finding it quite difficult to measure the output or the the result the

3:29  impact of the skill as well so I was kind of flying blind but I was you know iterating really fast um and um so that

3:39  project eventually sort of became the basis of PAC even though I didn't know

3:44  it at the time um and a lot of some tricks I had learned like building that

3:50  early set of skills. Actually, it's still open source if you want to if anybody wants to take a look. It's on my

3:56  GitHub like potato noodle n o d l e. Um, and in there you

4:02  will see some skills and a brain directory. [snorts] And so I was really interested in this idea of how do I, you

4:09  know, extract my own ability, if that makes sense, and give it to the agent,

4:14  right? cuz I was I I realized that you know all I was trying to do was trying to teach the agent to write code more

4:19  like me you know do do you do do workflows more like me. So you know the

4:24  skills were like an entry point to doing that. Um and then you know after I joined

4:31  cursor uh I was starting to work on the agents window and uh it had a lot of

4:36  performance issues. Uh it was it was it was pretty laggy. Uh and so since I had

4:41  experience working in React, I was asked like, "Hey, do you want to come and help out uh with the agents window?" Um and

4:48  so the the this beginning of the cursor journey was very manual. [snorts] Uh I

4:55  was deep in like looking at like flame graphs and heap snapshots and trying to

5:00  see like why exactly is the app so slow. Uh but then coming back to the same realization like you know I was sort of

5:07  the bottleneck. I was doing everything manually. I was sort of the meat proxy in a way, right? I was the meat proxy

5:13  between my agent and Chrome DevTools. Uh and I was like really annoyed by that.

5:18  And what month of the year is that? Let's say where are we in the timeline? Uh so I joined Cursor in March. So this

5:25  was like early early April probably early April is when [snorts] you know uh

5:30  I joined and I didn't have any skills, right? I had I I sort of abandoned my personal skills because I didn't think

5:36  they'd be relevant anymore. Uh but then working on the agents window uh and [snorts] now working on grockbot uh I

5:44  sort of realized that a lot of the lessons I had learned from those skill time building the the initial set of

5:50  skills were very relevant especially around things like verification

5:55  uh you know being very rigorous in your work um [clears throat] because I think

6:01  from my experience even the the frontier ones tend to

6:07  tend to take shortcuts. Uh they tend to do the easy thing. Uh so uh a lot of the

6:14  skills that I've built have been around how do I make the easy thing the right thing? You know, how do I make that the

6:20  best thing? The idea of sort of distilling your expertise and turning what you do every

6:28  day into processes, that's something that feels super familiar to me. That's exactly what I've been doing with the

6:34  skills. And I suppose there's something in that which is a lot of people think domain expertise is getting less useful

6:41  now as people uh start to rely more on AI where what do you think about that

6:47  just as a sort of vibe check before we start talking [laughter] I actually feel like domain expertise is

6:52  is more important than ever you know uh I think I wrote this on my ex at some

6:58  point but you know at times I sometimes think of you know AI as is like

7:05  especially as the models get smarter and smarter and more capable and the frontier models are just getting so good

7:10  like I [snorts] love Opus 5.5 by the way um uh you know as the models get really

7:17  really really good it almost becomes like the bottleneck is no longer the agent right it becomes your ability to

7:24  express your intent and your goals in a clear way that [snorts] the agent can understand and actually carry out and

7:33  That's why I think you know like people with a lot of domain expertise are extremely have a have a huge advantage

7:39  in my opinion especially if you're a little bit like you know tech technoc curious you know so I I think of people

7:46  like you know like uh like a doctor or a lawyer or you know someone who who has a

7:52  deep expertise in a particular non-engineering domain and [snorts] if they're actually just a little bit

7:57  techsavvy and they can figure out how to use agents they can actually build really really great products, right? If

8:04  they if they have a clear enough vision in their head and they can articulate it in a way that the agent can build it,

8:11  you know, I think that that is really the the bottleneck these days is is like

8:17  the transfer of your intent, right, and your vision to the agent.

8:23  Yeah. I've been obsessed with language basically since agents um dropped. are just obsessed 100% and thinking

8:30  constantly about the the composition of words, how I can make things sharper, what um what might be hidden in the

8:37  phrases that I'm using. And it's and finding what I love is when you find a

8:42  word that the agent then hooks on to and then goes, "Okay, I'm going to reinforce that word. I'm going to reuse that in my

8:49  thinking traces." You know, I found that with um TDD was an early example of that. a lot of chat about TDD recently

8:55  of like, you know, people say, should you use TDD with agents? Doesn't matter. What you're doing is you're getting the

9:00  agent to think about TDD, getting it to write tests, getting it to prioritize things in a different way than it did

9:06  before. And that's why sort of grilling, I think, works effectively. Grilling is a Yeah. Yeah. It it draws those words out

9:13  of you, right? or or at least it helps the agent understand your thinking so

9:19  that they can propose those words to you and you can pick up and say yes exactly that. Uh I've actually copied some of the the

9:25  tips that you've shared as well where you know one of my favorite ones that you've shared recently or or not or like

9:30  maybe in the past couple weeks is [snorts] about uh reducing or eliminating tautological tests. Like one

9:37  of my pet peeves of agents is like all of the useless tests that they write. And so, you know, that was one thing

9:44  where, you know, the word tutology, right, is is is I guess, you know, not many people necessarily know that if if

9:49  especially if English isn't your first language, but there's a lot of meaning to that word. And it's like it's almost

9:56  like compressed, right? Like you compress a lot of intent and meaning into words. And so I I I totally agree

10:04  with you. I think language I've always been interested in language actually uh like programming languages natural human

10:11  languages and how they came to be and it's so interesting that now with agents it's sort of like this meeting of

10:18  natural language with programming language but it's all it's all language out of the hood it's all communication

10:23  totally I did a drama degree right so you know I've been thinking about language and Shakespeare and stuff for a long time [laughter] and so this all

10:29  feels very familiar um so okay there's sort before we get into like because I think

10:36  the thing I want from you is like software factory stuff, right? Software

10:42  factory is the big buzzword. Software factory is the thing that I'm thinking about too. I'm sort of releasing a course in that direction too. And it's this sort of scaling yourself

10:50  up to un unrealistic numbers of PRs basically or PR numbers that sound

10:56  ridiculous to people who don't understand how this works. So where I want to get to is sort of from people

11:01  who are doing kind of like one to five agents today up to, you know, hundreds of agents running at once and how that

11:08  sort of functions. And so I'd love to hear about your metaphor of the Michelin Kitchen instead of the software factory

11:15  because I think that says a bit about the way you think about this stuff. Yes.

11:20  Yeah. I I I've I've never really liked the term software factory. Not because

11:25  you know it's not accurate but I think I think the a lot of people when they think factory right they don't

11:31  necessarily equate that with quality or craft right things which are very

11:36  important to me and a lot of people and technologists who work you know building products we care about the user

11:44  experience we care about the things we're building. So while so while I do think software factory is an apt term,

11:51  it also I guess maybe conjures up negative, you know, maybe sometimes negative connotations. So Michelin

11:58  Kitchen is the thing that I've sort of landed on where it's much more I feel like it's much more aspirational and uh

12:05  I like the metaphor a lot cuz you know I like food. I'm called potato of course [snorts] and I like cooking [laughter]

12:10  and I see a lot of parallels right like with food right when you're cooking a

12:15  meal for yourself for example [clears throat] it's both utilitarian like you're trying to just feed yourself

12:20  right and and survive uh but it can actually be transformed into art right

12:25  and that's what what a Michelin starred chef or even just a chef or a cook can

12:31  do with food is take something very ordinary and turn it into a delicious meal that you know takes you back to

12:38  your childhood days or something like that. Um and so it almost like mirrors

12:43  that trust letter that I talk about where uh you can sort of imagine your own journey as a home cook, right? Uh as

12:50  a home cook, you are doing all of the food, the cooking yourself. You cut all the vegetables, you do all the prep

12:57  work, you do all the cleanup, you know, you are the one man or one woman show

13:03  really. Um, and it's an interesting thought experiment like, okay, if you

13:09  were to cook a meal and then you add people, right, your your your partner trying to your brother, your sister, and

13:16  now suddenly you have your whole family in the kitchen. I think most people would get very stressed by that, right? The thought of, oh, so many people are

13:23  just mocking around in my kitchen. They have no no idea where all the utensils are. I have a max capacity of one person in

13:28  the kitchen. Yeah, absolutely. So, I feel like that that's really apt because when you ask yourself that question of

13:35  how do I go from being a solo cook, right, to having an army or even not not

13:41  even an army but a few sue chefs, right, that that are helping me in the kitchen. How do I think about dividing the work

13:48  in a way that makes sense? You know, I'm not dividing work just for the sake of it, but in a way that actually makes the

13:55  sum the to the better than, you know, the total of its parts. And so the Michelin kitchen metaphor to me like

14:02  works really well in that regard because you know as a chef you're you know if

14:08  you become a chef you're in a position where you're not necessarily cooking all the food yourself anymore but you are

14:14  thinking you're almost like the tech lead right for the kitchen where uh you

14:20  know chefs have to think about you know not just cooking but they have to basically organize the whole kitchen and they're like the CEO of the kitchen they

14:27  have to think about when do you order ingredients, how do you store them, how do you prepare them, when do they have

14:32  to be prepared, you know, it's a whole it's a whole job, right? That's not just cooking. Um, and I think that again it

14:39  mirrors so much of how engineers write code today where you are not writing the

14:45  code yourself anymore. You have agents, right? But you as the human are still responsible for the final outcome,

14:51  right? your name still is associated with the work that you do, your reputation and you know so how you set

14:58  up your kitchen right and how you set up your skills your environment your codebase I think are ultimately the new

15:07  ingredients that go into um building product

15:12  yeah I think what I love about your approach is the amount of focus that you put into the environment that the agent

15:18  operates in right because I think a lot of people they think, right, the agent is good. I'm probably not going to be

15:25  able to make it better. Let's just trust what these magic model people have put into the harness and the model

15:31  combination. Uh, there's nothing I can really do, like I can't mess about with claw codes internals or something or

15:36  whatever you're using. Um, but what I love about your approach, and it's

15:42  something I advocate for too, is that you can change the environment the agent operates in, right? you can make changes

15:48  in the codebase and also give it tools for verification as well and allow it to

15:54  verify its own work. So the thing I I loved about watching that talk is the amount of focus you put in verification

16:01  and like that is the lever that you can start to generate trust. Can you talk about that and what that concretely

16:07  looks like? Let's start like looking at practical ways that people can improve their own processes, their own kitchens.

16:14  Yeah, I've I've I've said this a lot actually that you know even if you don't use PAC or you know your skills I think

16:21  that the single most important skill that should be in your toolkit is

16:27  verification because without verification and for for by the way for those watching who don't know what that

16:33  means it's this idea that you can give you can sort of give your agent uh hands

16:38  and eyes in a way that's the the analogy I where the agent is able to run the code,

16:46  right? And actually [snorts] uh interact with it like a normal human user would and also do things like you

16:53  know debug it, you know, take traces and snapshots. Um and uh funnily enough like

17:00  that was actually the first skill I built when I joined Cursor. uh that gave me a lot of that was that was the thing

17:05  that actually started to let me ascend the trust ladder a little bit in a way that some of the other skills I had

17:11  looked at or built had not really let me do because no matter how good you know

17:17  some of the other skills were like the how skill, the why skill, the unsop skill were, I was still relying on me

17:24  right as the proxy between my agent and the output. So that you know if the

17:30  agent can't actually see the result of its work there's no way it can actually iterate right and so this is where

17:36  people start to talk about loops this idea of a loop and really I think the term loop you know seems kind of uh

17:43  almost abstract like people like what what what is a loop what is an agent loop but really to me like the most

17:50  important part of a loop that allows it to be a loop is the verification part

17:55  because the agent is able to to verify by its own work and uh you know that

18:01  takes you out of the equation where now I can actually do something like so the very one of the very first use cases I

18:07  had for verification was you know like the performance work that I was doing on cursors agent window and I want I wanted

18:14  to get to a point where I could do something called hill climbing uh which is a term that I I think the labs uh

18:20  talk about a lot which is this idea that you know you have some kind of rubric or a way to judge or score something And

18:28  now because you have a loop, you can have an agent continually try to make improvements to that. Uh I think

18:35  Carpathy, Andre Carpathy also famously released uh something called auto research that has a lot of these ideas.

18:43  Um but yeah, verification I would say is probably the most important skill in PAC

18:49  uh and many [clears throat] other you know tool sets. Uh and I think it's the

18:55  most important thing to focus on. So a lot of the a lot of I spent a lot of

19:00  time actually you know tuning the verification the creative verification skill um and also internally the the we

19:09  have so many verification skills now like every app that cursor has or spaceexai has has a uh verification

19:16  skill that is automaintained as well [clears throat] uh and it's become critical infrastructure for our team because

19:22  everybody uses it and you went pretty far with that too right like you had a um in your talk I

19:28  saw that you actually built a custom CLI for that too. So what does that CLI do? Like how does it [clears throat] execute things and why did you I mean that's

19:35  proof of how deep you're going right of how much you're pushing that. Yeah. So this is actually a tip I

19:42  learned early on where um I guess you know back in January or

19:49  or late last year the thing that people were concerned about was context window, right? That was the big the big topic at

19:56  the time was how do I you know manage the context window because you know compaction summarization wasn't really

20:02  that good yet [snorts] and people were always people had this there was almost this meme in the community that you know

20:09  once your agent summarized or compacted once it would become sort of stupid

20:15  right for the rest of your session. So there was a lot of thinking around like

20:20  you know being very efficient with your context usage and so that was actually the inspiration for some of the uh the

20:28  CLI work inside of the verification skills. I guess now it's less so about

20:34  context because uh you know agents are much better or harnesses have gotten a

20:40  lot better with summarization. Um, I still think there's some benefits

20:45  to, you know, uh, having a clean context window. Uh, so the CLI is really just

20:51  more of a way for me to take the deterministic parts of what the skill does and encode that into a script or

20:58  CLI to reduce to kind of take away the judgment that would otherwise

21:05  unnecessarily be used because with judgment so I also think of you know

21:10  agents and skills in sort of like it's like a gradient

21:15  you have some parts of the work that are entirely judge measurement based right you know something that requires thought

21:22  you know putting together multiple pieces of context thinking um and then you have the more deterministic parts

21:28  like I don't know if you wanted to uh refactor some code right from one

21:34  pattern to another that's very mechanical right you don't you don't need an agent to think about it and come

21:40  up with it in a novel way each time right and so that that was really the inspiration for the CLI and you'll see

21:47  this in a lot of the other skills that I built is like I try to extract out the deterministic parts and turn that into

21:54  code and just leave only the parts that actually require judgment to the agent.

22:00  So in a way I think of the seal as kind of like your wrapper, right? It's a wrapper with some light instructions around how to use these custom tools

22:06  that are inside of the skill. Um but yeah, I don't think the CL is really that interesting in its own really. It's

22:13  not like a novel piece of software. It's just something that interacts with like Playright and the Chrome DevTools

22:20  protocol and calls a bunch of APIs. It's like it's just a bunch of glue. No, it's fascinating because it's a way

22:25  of hiding information from the skill, right? It's a way of conserving the skill, keeping the skill quite small, I

22:31  imagine, and then you're able to delegate more of the complicated deterministic stuff into a script within

22:36  the skill. So it's almost you're compressing information and making the

22:41  agent do more consistent things more consistently. Yeah, that's fascinating.

22:47  And it it [clears throat] also helps I guess if you care about context window it it does help because now the agent

22:53  doesn't need to uh you know re reinvent uh things cuz uh one thing I had noticed

22:59  early on when we didn't have a CLI was that uh well the the agent would try

23:05  to verify it work but it would basically rebuild the world each time and then every agent did it differently and I was

23:11  starting to notice like that's very inefficient right I was wasting it it was actually not just about context

23:16  usage but also speed, right? Like because now an agent had to actually go off and write the scripts or the CLI and

23:22  test it and you know and it doesn't work and the last agent did it and it worked but it discarded it. So it was just very

23:28  obvious at that point like I should just turn this into a CLI and put that inside of the skill uh so that every agent that

23:35  uses it now benefits from that same piece. Um but I I also think like you

23:42  know it's a good push for people to think about is how much of your skills and rules could actually be

23:48  deterministic. Um that's like another core thing or or

23:53  one of my core principles that I like to think about is yeah how do I uh make

23:59  very efficient use of determinism and non-determinism and you know let Asians shine at the

24:07  non-deterministic parts right because that's what they're trained to do. Um and the other parts which are much more

24:14  mechanical or you know straightforward can be just pure determinism. Um, and

24:19  you'll see this as well for things like doing migrations. Um, which is another big thing that I've I've talked about

24:26  is, you know, going from one technology to another, especially one that is

24:32  better for agents, right? And a lot of how you can do that migration is, I think, through things like scripts and

24:38  CLIs, like the deterministic parts like code mods, you know, like crawling the

24:44  abstract syntax tree and transforming code literally mechanically, right? like a script does it for you instead of the

24:50  agent. Totally makes sense. I I mean I think

24:55  what there's another thing there which is you're taking stuff away from the

25:00  agent and you're kind of putting it in the environment too a little bit which

25:05  is let's say you have a a thing that you notice the agent always gets wrong. You want to make that um just impossible

25:13  within the environment. And that sort of comes down to code quality as well. I

25:18  mean, I talk about a lot like having a what a good codebase means, right? What

25:24  is a good codebase? And there's a definition I like which is a a good codebase is a codebase that's easy to

25:30  make changes in, right? Easy to um change stuff without things screwing up.

25:36  And that means that you have a lot of guard rails that you have a lot of um the agent or the human is constrained to

25:42  very narrow paths. And that's again something you talk about in your talk. And you talk about this not only on the

25:48  kind of sort of automated checks side of things. So linting and type checking blah blah blah but also in the way you

25:55  design abstractions. And you guys even I think built a framework uh for your agent to work in too.

26:01  I think what I'd love to hear is you obviously think of that as very important, right? And that's how

26:08  important is that compared to other things you could be doing like building features or shipping work.

26:14  Yeah, I think that's a um I almost feel like the new job of the engineer is really to to spend time on the

26:21  environment. Um I almost actually wrote a tweet about this yesterday, but I but I didn't. But I think that

26:29  I think that you you know if you if you haven't really spent time, you know, building trust in your agents and

26:34  building skills and tools, you can get stuck in this mode where you're very low on that trust ladder, right? you don't

26:41  have a lot of trust in your agents work. And so the only way to cope in that when

26:47  you're in that situation is just to kind of lock in and micromanage your agents. And that's very time consuming. And when

26:53  you're stuck in that mode, you don't really have the luxury to think about, you know,

27:00  uh higher level things like like making yourself more productive. In the same

27:05  way that uh I guess analogy would be like if you've never taken the time to

27:11  learn like your tools right as a developer when you were writing code yourself and you know you've never heard

27:17  of VS Code, you've never heard of Vim, you only knew about Notepad [laughter] uh and you had hadn't even heard about

27:23  Git. That's sort of the analogy. It's like you you haven't spent the time sharpening your own knives, right? And

27:29  so, of course, if you have a dull knife, then everything's going to take a long time. Um, and you're going to be you're

27:36  just going to be and and especially if you know deadlines are looming, then you don't have the now you're stuck in this

27:42  rut, right? Where where you you you don't have sharp knives, you don't have good tools, but you're under all this

27:49  pressure to ship, right? And so, all you can do is just focus on that. But I do think that, you know, if you can find

27:55  yourself the time to actually spend time thinking about your setup, it's again

28:00  going back to the cooking, you know, analogy, it's like uh, you know, if you, for

28:06  example, if if cutting cutting cutting the garlic is like super slow, right?

28:11  There are garlic mashers, right? You can you can buy and you put it in the thing and you like squeeze it out, right? It's

28:17  super fast. Uh, machines and tools were invented for a reason, right? And so if

28:22  you're operating a Michelin kitchen and your your your cooks had no tools, then

28:27  of course everything's going to be extremely inefficient, very very, you know, every every every cook is going to

28:33  make something up of their own. So I think the tools and the determinism to me are you know taking that part away

28:41  and and just like you said about constraints as well. It's the constraints are are to me as well like

28:48  uh actually a slight tangent on that is uh I think we should talk about TypeScript cuz like we we actually both

28:55  share like a background in Typescript where you know you obviously have done a lot of work with TypeScript and total TypeScript and you know you're a leader

29:02  in that space and I uh had adopted TypeScript pretty early and I had given

29:07  like a talk or two at Typescript conf uh many years ago and so one of the the

29:13  talk that I did actually was about type systems and constraining the

29:18  constraining types. Like one of my most favorite things about Typescript is actually type narrowing, right? This

29:23  idea that you go from a very broad type, right? That could be anything and then you through type guards and you know

29:31  type narrowing and you know runtime checks you can actually narrow the space and say like oh this isn't just a string

29:38  this is a very special type of string. It's a constant, right? like I but I I determine that through the type system

29:45  and in a way it's like uh there's a lot of parallels I think to that with constraints in your codebase where is it

29:52  you're you're constraining the space right if you if you think about category theory as well you know you're

29:58  constraining the the number of possible types right that can can exist

30:05  and you're saying there's only one type right and for for us like that framework

30:10  that I'm called Dune. Uh it's not an open source framework. It's the the way

30:15  I describe it to people. It's it's kind of like a internal Nex.js for our Electron apps. Uh but it comes with a

30:23  lot of really really restrictive lit rules and the codebase is designed in a way that there's really only one way to

30:30  do something. So we make use a we make use of a lot of conventional

30:35  patterns. So like features all go into a specific directory. Well, every feature

30:41  has its own directory. As an example, you know, there's like a a thing that discovers features like through a

30:46  registry and like crawling the codebase and stuff like that. But this

30:51  conventional pattern and the lint rules make for an environment where it's

30:57  actually very hard to write bad code. And that sort of frees up the it both

31:04  frees up your own mental uh you know capacity as well as the agent sort of

31:11  doesn't have to think about that anymore where it's just like oh there's only there's I should just if I want to add a

31:17  new feature it just goes in the feature the new feature directory and all the code goes in there and I'm not going to

31:22  append to a god file right that was really actually the inspiration for those feature directories is the very

31:29  first couple of versions of Grockbot were composed of like eight god files

31:36  which were like at least 10,000 lines long if not longer and so I kind of had to break it up into smaller pieces.

31:43  Uh but it was just observing you know actually that's another important part is observing how agents fail and then

31:50  every time you see a mistake every time you see something that could be done better you think you step back and think

31:57  how do I turn this into a lint rule? How do I make it so that the code base makes this impossible? Right? And it comes

32:03  back to me for my you know my background learning Typescript and types uh type

32:08  systems is how do I constrain the space so that you know I know precisely what

32:15  I'm working with and I think yeah there's a lot of parallels there. Totally makes sense. And don't I mean

32:21  it's funny that you mentioned TypeScript and Goth files in the same sentence because Typescript famously has a 25,000line type uh file.

32:29  [laughter] Although I don't know if they've rewritten that and go as they probably have, haven't they? Um,

32:34  okay. So, environment is important. You should watch your agent like a hawk to make sure that any mistakes it makes.

32:42  You turn them into things in the environment. And the benefit of the environment is you're not overloading your agent, right, in terms of rules, in

32:49  terms of things it has to remember. It's just in the environment. And so it stumbles into the rules and exactly um

32:56  you know bounces off them and hits them at the right moment. So okay, we still haven't talked about

33:01  the 2,500 PRs. Where do those come from? Like how do you you've built your trust ladder, you've worked on your

33:07  environment, and you understand, okay, um I now want to scale up. So what are

33:13  the mechanics of that scaling? Are you um initiating 2500

33:19  like chats per month? That can't be right. So there must be are there any kind of automated triggers that trigger

33:26  stuff in your repo? Like how do you get the software factory kind of triggering work by itself?

33:32  Right. Um I'll definitely say that the prerequisite to you know something like

33:40  a very high volume of of pull requests um is the environment. you know, the the

33:46  stuff we just talked about where I definitely would not have been able to do this if I had not spent the time, you

33:52  know, thinking about the kitchen, right, and the knives and the tools for my Asians. And so, in a way, I I think of

33:58  this as I've spent the time building one kitchen and one restaurant. And now I I'm in a

34:05  position where I don't actually have to be there anymore because the environment, you know, that the same

34:12  analogy, right? It works really well. [laughter] Yeah. You open chain of restaurants, right? That's Yeah. Exactly. Yeah. Exactly. It's like

34:19  you're Gordon Ramsay and you know, you you've taught your executive chef like all the tricks of the of coming up with

34:25  great menu. Uh and like the kitchen is set up really well. Everything's just perfect and you're now in a position

34:32  where you can open your second your third restaurant. And [snorts] I guess I I sort of see each project

34:38  that I work on, like each big chat is sort of like a restaurant, right? and and I'm I'm I have multiple of them

34:45  operating at the same time and I'm sort of like helicoptering between them

34:50  sometimes some more than others depending on how in the loop I am but yeah definitely I think there's there

34:56  there are external triggers and context that those projects don't have that

35:05  for a long time I was the proxy for that so uh the best example I have is like you know you have a project that's

35:11  working on a feature uh or you're trying to fix a bug and you're getting bug reports, but the bug

35:17  reports are going to things like Slack or linear or X, right? And these are

35:24  external systems that aren't connected to your inner loop. So, I like to talk about this outer loop and the inner

35:30  loop. Uh I don't know if I'm using the definition correctly but to me my inner loop is like basically my engineers my

35:38  agent engineers working on the code to an building towards an intent or

35:45  snapshot of my intent right and the thing about that is that the snapshot can go stale right new information comes

35:52  to light that I then have to be the proxy of and you know transfer that context to my agent so you know if you

35:59  if you don't have these triggers pulling information back into the interloop, then you sort of have to play that role

36:07  where you're you're off, you know, in Slack or X or or whatever and you're gathering context, right? You're getting

36:14  context about bug reports, about feature requests, about, you know, something someone said about, you know, our

36:20  backend infrastructure has some limitation, you know, all that information, you have to f that across

36:27  to your agent. So that's where I think like tools like Grogbot are really good

36:32  because they help you automate the outer loop as well. And when you connect those

36:37  two loops, it's very very powerful because now all of a sudden your agents have the ability to get context for this

36:44  for themselves, right? If for example uh you know either through just as a

36:51  simple example like maybe you have the Slack MCP, right? Or you have uh your own harness, right, that you've built a

36:58  Slack subscription into for a particular Slack channel. Now all of a sudden you

37:03  can tell your agents, okay, subscribe to the Slack channel. Every time there's a uh, you know, bug report about

37:11  something, go off and triage that thing, right? Go reproduce the issue, right?

37:16  Using the verification skills that we've already spent time building and all of those other skills that we've set up so

37:22  that I have a lot of trust, right? I have a lot of trust that these agents can actually go off and understand the

37:28  bug, you know, uh verify that the bug actually still exists on main and it

37:34  wasn't something about you maybe the users setup or their data or maybe I don't

37:40  know they didn't install a dependency or something like that like uh basically I think uh creating that yeah creating

37:49  those two loops and connecting them is really a very important part of the job these days. Um, especially if you are

37:56  thinking about how to scale yourself. So, a big theme here is really just like

38:01  always thinking about like what where am I the bottleneck in this process? Why do

38:07  my agents need me, you know, to answer this question? I I always like to think about that. And so I try to think about

38:13  how do I actually get the agent to answer its own question, right? But not by hallucinating, not by guessing, but

38:19  actually real data. And you know, a lot of people talk about this idea of a company brain, right, or a context

38:25  graph. I feel like those terms are unnecessarily complex uh or even abstract. To me, it's

38:33  just about um how do I take information that my agent needs that I would

38:39  otherwise have to go and pass it myself and just teach it how to do it, right?

38:44  And that removes me from the equation. And so how I arrive at 2,000 or however

38:50  many PRs is the fact that I have all these loops set up, right? And so uh it

38:57  allows me to open chain restaurants, right? I can I can really parallels

39:02  myself. So yeah, I'm not sitting there creating 2,500 chats, right? Of course, it's really like these projects are um

39:10  actually cursor has a new feature called projects which are these like coordinator agents. Um and so the

39:17  coordination co coordinator agents are really good at sort of delegating and not doing work of their own but they

39:23  manage and supervise like almost a list of tasks and they spawn sub agents to go and do them. And so I'm just constantly

39:30  feeding context or teaching the agents how to get their own context and then they're going off and doing the work for

39:35  me. Uh and really the big the last thing I'll say to this is like the big unlock for me for getting to 2,000 PRs is

39:43  starting from the question and working backwards of how do I get to the point where my agent can merge its own code?

39:51  Because the obvious thing people ask me when when they when I tell them, "Oh, I

39:56  shipped 2,000 and 2,500 pull requests last month." They'll be like, "How did you review that?" Right? That that's a

40:02  lot of PRs to review. Like your team must hate you. Do do you mind if we go there in a second? Because a good question about

40:09  that. Yeah. Yeah. Yeah. I want to like this analogy is great. I want to like deepen it a bit which is

40:15  before if you're like manually initiating all those chats it's like you're bringing the orders to your chefs

40:20  manually right whereas if you've got an agent sort of like doing the expo then you're able to sort of run it yourself

40:26  itself what is what does that concretely look like then you've got these sort of grock bots that are um subscribing to

40:33  channels pulling in Slack messages and you it sounds like have a couple of coordinator agents or like chief of

40:39  staff agents that like monitor that or something like when you look at your

40:45  computer to manage your agents, what does it look like? Yeah. So, [clears throat] so uh this is

40:52  I guess somewhat confusing but we're working on you know simplifying and unifying but so uh there's graphbot uh

40:59  which or you know you can use other tools of course as well but I I largely think of these tools as like your outer

41:05  loop. These are tools like you know Grabbot that have connectors right these are connectors I guess they a lot of

41:11  people call them personal agents um but they're connectors to things like your email your calendar slack uh plaid I

41:20  don't know like all these different services and they are a great source of pulling context in to your work so the

41:29  same way that a human like you know if I were if I was a manager and I was leading a team of engineers years. Um,

41:37  you know, like when I used to work in Netflix, one of the biggest things that managers would talk about was this idea of context not control, which funnily

41:45  enough, you know, has so much uh has so much uh carry over to the agents world.

41:51  Uh, of you know, you you know, you you of course can drive to an outcome you want by control, right? Like by

41:58  micromanaging, but what you want is to provide context instead, right? like teach the agent, teach your engineers

42:04  how to be self-sufficient and then you don't have to micromanage them. Um, and so I see a lot of parallels

42:11  there. Uh, but yeah, graphbot. So, concretely, I have some graph bots that

42:16  look at my Slack channels, look at my X, uh, or my emails, uh, or linear, and

42:23  they're just constantly they have routines that subscribe. So they're constantly watching and I have I I'll

42:29  tell them things like you know uh I'll watch for issues with uh bugs in the

42:34  graphbot desktop app as an example. Uh and whenever you find that send it to my

42:40  cursor project. So one of the really cool things about grabbot is it connects to cursor. So cursor has uh like I I

42:47  just mentioned this new feature called projects. And a project is really a uh again like a you get a coordinator agent

42:55  that's in the cloud. It has its own computer and all it really does is like it's a manager of agents. It's like your

43:01  executive chef, right? Your your chief of staff. It doesn't do the work itself. It delegates and orchestrates and

43:08  manages the work of other sub agents to you know that report to your chief your

43:16  chief uh of staff. And it basically is responsible for driving the work forward

43:22  and managing things and uh passing context to them. So if you get a sudden burst of issues,

43:28  let's say you get 30 issues at once in one payload or something or very quickly the coordinator agent can figure it out

43:34  and delegate. Yeah, exactly. It gets like uh you know 30 the 30 or so payloads and spawns a

43:39  sub agent or a single coordinator agent. It can actually do a bunch of different topologies of agents and it will sort of

43:46  figure out the best way to uh you know efficiently distribute the tasks to your

43:52  team of agents. Um so I use uh cursor

43:57  projects a lot um and I also use grapot a lot and cursor projects are my inner

44:03  loop and grabbot is my outer loop. Grabbot takes all the context, external context, gives it to the projects

44:11  because it can actually just send messages to those projects, right? You don't even have to open cursor. You can

44:16  just tell your grabbot, okay, create a project, right, for these series of tasks. They're all related, right? Maybe

44:23  as an example, you know, you've had a uh [clears throat] a big burst of issues that are all about performance, right?

44:29  Your app is slow uh and they're all connected, right? Maybe some of them even have a similar fix, right? But and

44:38  you can certainly go off and just spawn one agent per task, but then you've lost that sort of thread between them, right?

44:45  And and you may duplicate work or you may not really think about the higher level problem. You know, sometimes when

44:50  you you you solve bugs, you know, it helps to have multiple bug reports that are are slightly different because it

44:56  helps you really, you know, zoom out and see actually, you know, the problem when I looked at this one report, I thought the bug was here, but actually when when

45:03  I see the other multitude of bugs is actually up here, right? Yeah. Got you. So that that's why you

45:09  have so many agents in that loop then, right? Because it's not just you have um like you have a bug report comes in, you

45:15  spawn a single agent to look at that bug report. that a that single agent will be duplicating work with other um other

45:21  agents, right? Because if there are multiple bug reports coming in through the same thing, that can be duplicated work. Yeah. Fascinating. [snorts]

45:28  That's really fascinating. Okay. And so this just this endless series of triggers um coming from real users

45:34  reporting real reports um builds up this sort of and accelerates the factory sort

45:40  of adds more orders in. Other than bug reports, are there any other sources that you use for like um accelerating

45:48  for pushing these PRs? Uh well, funnily enough, it's some of it

45:54  comes from uh reading the code, too. So, I guess I have sort of uh well, so to

46:01  clarify that, you know, the 2,500 PRs, they're not obviously like 2,500 features, right? they are a lot of the

46:08  work actually is spent on gardening like another term that I really love. Uh

46:15  where so I guess this is more important when you have a big team of engineers human

46:21  engineers that you work with where and also this goes back a little bit to what I was talking about with the

46:27  environment. You know, setting up a really good environment that doesn't just help you and your agents, but everybody on your team, right? Think of

46:33  a new hire who doesn't have a lot of context on all of your engineering practices joining your your team. And if

46:39  you have a really good environment, they can be productive from day one, right? They can they don't have to like, you know, make open a bunch of lowquality

46:46  PRs. They can start, you know, they can start just turning out really good code.

46:52  Um, and uh, yeah, I think I I sort of lost

46:57  my train of thought. I've got a I've got a followup, which is what's what are the mechanics of like triggering

47:03  like how when when do you trigger a a agent to go and look at the code, right?

47:10  Because some people might say, "Oh, let's just do that every hour or something or like on a chron job or

47:15  what's Oh, yeah. Yeah. Yeah. Yeah. Uh I saw some of your recent tweets as well about like you know the some of the tweets

47:22  you've been doing which are great for setting up your routines. Uh I have some

47:27  routines like that as well. Um so uh one of them is uh

47:35  like looking through just another simple example is you know [clears throat] React has a lot of foot guns. Um, so,

47:43  uh, as as I'm sure you're aware. And so I have an agent that's just constantly looking for band patterns. And the

47:50  interesting thing about that one is that I don't actually tell it to fix the issue first. I tell it to append it to a

47:55  document. And then every couple of days I look at it and I see actually these are all the same thing, you know, and so

48:02  that gives me, you know, you almost want like a buffer, a queue. Sometimes that's actually more effective than just

48:09  spawning off a couple of like a lot of sub agents to fix every single thing because when you are [clears throat] in

48:15  kind of pure execution mode and just trying to like you know f uh you know execute on the orders that are coming in

48:21  very fast you sometimes miss the big picture. So sometimes having a buffer

48:26  forces you to think about the big picture because you you you have these artifacts and things that you can look

48:33  at as a human um and sort of use your own human judgment to or I guess you can

48:39  use an agent to do that as well. But you give the [clears throat] agent and yourself a way to identify patterns,

48:46  right, that you might otherwise miss if you're just only solving each bug at a

48:51  time. And that's also really the benefit of having something like a chief of staff agent is uh it can see the forest

48:59  right uh in addition to actually doing the execution.

49:04  Fascinating. That's I mean my brain is exploding a bit there with the sort of chief of staff at the software factory.

49:10  I might have to change some of the course that I'm filming next week. That's [laughter]

49:15  uh all right. Let's talk about let's talk about review, right? because this is the reply that you get, you know, is

49:20  did you read did you taste all 2500 of those dishes as they swept past you?

49:27  And I assume the answer is a variety is a version of no.

49:34  Yeah, I think you you you don't want to be in a position where you're not tasting your food ever again. Uh but you

49:40  also, you know, for scale, you cannot be tasting every single dish that comes out of your kitchen, especially if you have

49:46  multiple restaurants. So it becomes more about sampling right and thinking about the processes in the same way that you

49:53  know if I guess maybe this is where the the the factory analogy is a bit more

49:58  apt is you know as a quality supervisor on a factory you you can't look at every

50:04  single item you sample right you take you you you go in there every day and you look at the quality of the pull

50:11  requests you look at the code that the agents are writing and you scrutinize it

50:16  very rig rigorously and you think about all the inefficiencies, the bad patterns

50:21  that the agents are doing and then you think about how to course correct the environment, right? Not not that single

50:28  agent. Uh because if maybe if it if it was a one-off incident, it's fine. You

50:35  know that maybe there's nothing to fix there. But if you actually notice that multiple agents are are having the same

50:41  issue, right? They're taking the same shortcut. they're they're propagating the same workaround everywhere. Uh

50:48  that's a sign that you should go off and think about how to uh amend your kitchen

50:53  or your factory, right? Like thinking about your skills, your constraints, your lints, your type systems um and

51:02  setting or adjusting it so that that problem doesn't happen again. And when you do that enough times, then you get

51:08  to a place where the codebase is again like the environment is so constrained

51:13  and so it guides you so well that you can just you can just step away, right?

51:19  That's the dream. And I'll I'll definitely say it um it's very hard to get to this point. I don't want to sell

51:26  this as like, you know, something that you can just do easily by using PAC. Like it takes a lot of time and effort

51:32  to think about your code and where you see your agents failing and thinking

51:38  very thoughtfully, intentionally and setting up guard rails and constraints

51:43  so that they do the right thing by default. And you're not [clears throat] like if

51:49  to go back to the software factory analogy, this isn't a dark factory, right? This the lights are on, right?

51:55  It kind of is. Yeah, actually. Is it? Yeah. Well, it's dark in the sense that so um it's dark in the sense that well I

52:02  think if my agents are merging their own pull requests it's sort of become dark where I go to sleep my agents now work

52:09  24/7 uh I have I have the equivalent of like more than 10 chiefs of staff right each

52:16  working on a different area like for example I have one that's working on performance of the Grockbot desktop app

52:23  I have one that's working on uh fixing bugs that users report I have one that's

52:28  exploring rewriting it in a different language just for fun, you know, like what if what if, you know, just

52:34  reimagining what what it would be if it was like a native app. It's just a toy. Um, but the idea is like yeah, I uh I

52:41  when you spend the time setting up your environment, I've gotten to a point where I review the pull request after

52:47  it's landed, right? I I tell my agents full autopilot is is something that you

52:52  can do in in PAC and that will trigger off this very intense rigorous

52:58  verification loop where it will spawn a bunch of verifier agents for every pull request and it will fuzz right fuzzing

53:06  meaning that it will actually run the application. It's going to click around and try to use it like a real human.

53:11  look for regressions, look for bugs in your implementation and um it will try

53:17  to find issues with the thing and then it will fix it itself. It'll do that again and eventually get the PR to a

53:24  state where it can land. Uh so it does it does it is quite token

53:29  intensive. You can tune this of course. Uh so you know instead of like 10 verifier agents you might do like one,

53:37  right? Or you just tell the agent to verify it's done work. But yeah, the key thing is the verification part is really

53:44  the key piece that gives me a lot of confidence that I guess verification plus the environment, right? It's these the

53:51  combination of these two things that allow me to step away and say agents go off and merge your thing. I'll review it

53:56  in the morning by looking at my commit history and if I see problems, I go and course

54:02  correct, right? And I'll go and revert or modify, add new link rules and whatever. Um, so

54:10  it does it does take time to get to that point, but once you get it, oh, it's so it feels so magical. Uh, I I I tell

54:17  people like I'm sleeping so much better now because, you know, it took it the

54:22  very first day I turned on the sort of dark factory was very scary because I was like, "Ooh, what if I call the SE,

54:28  right? What if I break something overnight?" Uh, and it took a lot of it took a lot

54:34  of uh bravery, I think, to do that, but somehow I did it. And yeah, now I'm in a

54:39  place where my Asians are are merging their own code while I sleep. It sounds like

54:44  I think it's dark in that sense. Yes, it's dark sometimes, right? You do sometimes. That's true. That's true.

54:49  Because I think of a dark factory is like almost like if you take the original definition of Kapathy's vibe

54:55  coding, right, which is the code almost doesn't exist. You forget that code might be a thing. I think your approach

55:01  is totally different from that, which is that code and the environment is essential. And if the code in the

55:07  environment are bad, then you will get bad outputs. Garbage in, garbage out. So I I I think this is a this is a

55:15  different thing. It's like, you know, the I don't know, maybe there's a dimmer

55:20  switch or something, right? Like, you know, some parts of dark, some parts were light. This is why the maybe the the kitchen is a better analogy

55:27  the restaurant because you know even as a as a as a as a [clears throat] restaurant

55:33  restaurant you still might go to your restaurants every now and then to take take a peek in taste the food right

55:40  uh I think that's the idea of sampling instead of blocking I think is really important I think what would you say to people who

55:46  are in I guess you're obviously in a pretty security conscious environment where you're working very security

55:52  conscious mh [clears throat] Um maybe there are folks working in like um medical

55:58  applications or law or finance or something. I think of the like some PRs

56:04  are kind of like two-way doors which is you can merge it and then revert it, right? It's cheap back through. But

56:10  there are some PRs that are one-way doors, right? That will cause data loss of some kind that will

56:16  do something that can't be easily walked back. How do you deal with situations where most of your PRs, let's say, are

56:23  one-way doors? Like, is this something you just wouldn't recommend or like what do you think? Yeah, I think that's a really good

56:30  question. I think that it all comes back to me to the quality of the verification that you're able to

56:37  um get out of your agent. And I think for domains where the work is

56:44  verifiable, this is easier, right? and the the oneway doors become two-way doors in a

56:51  sense. But I guess I don't know if you're working on something that is like extremely

56:57  is very hard to verify programmatically then I think yeah you're definitely in a position where it's very hard to get to

57:04  that point. Um so I do think like yeah verifiability of the domain is an

57:10  important aspect to be able to do this. Um and software engineering is just one of those things where it's quite

57:16  verifiable in in a lot of cases maybe not totally um you know like other

57:22  domains like mathematics I think are another example of not all of it of course but some aspects of mathematics

57:30  can be verifiable if you write a proof for example um and

57:35  so yeah I think it's a great question that I don't really have the answer to and I think that this is something the

57:41  industry and us as engineers will have to figure out is you know my sort of uh

57:48  hope and prediction for the future is that we'll see more and more interesting new agentoriented programming languages

57:56  and one of the most fascinating ones that I've seen so far is this one called bend bend d bend um and that language is

58:04  one where it kind of marries programming with proofs right there used to be a

58:12  time, you know, where you actually had to write your proofs in a different language. And proofs, by the way, for

58:18  those uh who who aren't familiar is this idea of uh that you can sort of formally

58:24  verify that some code is correct mathematically, right? Especially if

58:29  you've written your code in a very functional programming way.

58:34  uh but for the longest time you had to do that in a separate language like lean or tla+ or uh I'm blanking on some of

58:42  the other other examples but uh like languages like that where you would construct the mathematical proof and

58:48  then use a solver essentially to det that that you've covered all the cases

58:54  you don't have like a race condition or or whatever. So yeah, I think

59:02  trying to sum up the question, I think yeah, if you are in a position where you can figure out how your agents can truly

59:07  verify the work in a way that gives you confidence, you can actually, you know,

59:13  uh have the PRs merge cuz if it compiles, right, if it if the proofs show you that it's correct, then why

59:21  wouldn't you just merge it? Um but of course, yeah, not all the means are

59:26  verifiable. Yeah, it's a tough one. Um, okay. I think we've got to think about

59:34  wrapping up because we are nearly on the hour. Have you Have you got something after this? I mean, I've got something before I give my son dinner, but

59:40  I I can go a bit longer after you. Okay, let's let's go five minutes longer then. Um I think I just want to have one

59:46  more question which is I think I want to ask how you see Pstack

59:55  and how you see skills in general like in terms of we talked about this before

1:00:00  we went on air which is like people think of as like my skills versus your skills and how do you combine frameworks

1:00:08  together? How do you use Pstack with my stuff? like what should you take from each one and because I think I see

1:00:16  skills as sort of just derived from process basically like they're just

1:00:21  processes turned into words and I would love to know

1:00:27  how you recommend people take Pstack and take my stuff as well and turn it into their own processes.

1:00:35  I think you shared a tip actually today that I thought was actually very relevant, which is this idea that you go

1:00:40  off and look at your previous transcripts, right? And you sort of mine for information of, you know, your own

1:00:48  look through your own your own prompts, right, to the agents where you correct them where you have to constantly

1:00:53  intervene and uh you know take that higher level learning and turn that into

1:00:59  a a reusable skill, right? So that agents stop repeating that mistake. I

1:01:04  think that uh PAC and your skills are very complimementaryary. I I totally

1:01:10  agree with you that they're like a skill is really much just process. I mean it's just at the end of the day a skill is

1:01:15  just English or or language. It's just markdown. Um and I think you can you can

1:01:21  definitely weave them, combine them in a way that makes sense to you. But I do

1:01:27  think that uh everyone should have their own set of knives, right?

1:01:33  I I keep going back to the the the cooking analogy, but it's so apt because like, you know, every chef when they go

1:01:39  to a different job, right, when they go to a different restaurant, they carry they bring their knives with them. The tools go with them, right? And so trust

1:01:46  to me is really about trust in your own tools. And when you spend the time sharpening them and understanding them

1:01:52  really, really well, you can do great things. And everybody's skills and tool set is going to look different. you

1:01:58  know, someone might find a lot of success combining, you know, like your grill me with docs, uh, or wayfinder

1:02:05  skill with some of the execution skills in Pstack as an example. Some people might use more of your skills, some

1:02:11  people might use more of my skills. I think at the end end of the day, it really just comes back to how much do

1:02:17  you trust, you know, me and Matt, right? Like if you if you trust us both, of course, use our skills, but I also

1:02:23  encourage you to, you know, look at your own transcripts. Um um tell the agent to

1:02:29  look through, you know, some of the all of the patterns that you've used, the the times you've had to intervene, you

1:02:36  know, suggest turning them into lint rules or new skills, right? The the past

1:02:41  chats I I often say is like a a treasure trove of context because that, you know, it's it's like the process materialized,

1:02:51  right? Like it's the real process. It's not an abstract idea in your head. it's the actual thing right and you can

1:02:57  actually see how it happened in practice and extract so much information from that and there's so much so that I

1:03:02  actually turn I have a skill in pac called recall which is exactly that um where this was a pattern where

1:03:10  you know I was working in I was working on a similar problem so specifically I was working on virtualization for the

1:03:17  cursor application and there were a lot of bugs and so you know every time I started a new chat I was like ah this

1:03:22  there's so much good context from the last one So, you know, I want to bring it over to the new chat. How do I do that? And that's where the transcript

1:03:29  came, uh, you know, looking at the past transcript came about. And then recall was just a way for me to collapse

1:03:35  collapse and compress that workflow into a skill. So that I didn't have to just say I didn't have to write a long essay

1:03:42  every time. Go look at all these chats, right? And, you know, blah blah blah. So, I I largely think of skills,

1:03:47  especially as agents get more capable as really encoding workflows. you know

1:03:52  skills from last year were really more about like almost like implementation details like here are the exact script

1:03:59  commands you know you should use right I think with the latest models you can

1:04:04  just delete those parts and just focus on the workflow right until it it's more the skill becomes more like a

1:04:11  series of steps a series of your process uh and I think

1:04:16  over time we'll see that skills get smaller and smaller you know more compact Um, and yeah, they're very

1:04:24  compatible. Or you can, you know, if you want, why not read our skills, right, and com and combine them in your of your

1:04:31  own, right? Combine Wfinder with potato mode and make your own custom mode, right? Like like skills are the the

1:04:38  thing I love about skills that is are that they're so malleable. You can do anything you want. It's just language.

1:04:44  Absolutely. There's nothing magical in them, right? They're just words. And Exactly. If if there is any magic in them, it's just the words chosen and the

1:04:52  phrases used and the thinking that's been done to turn those like take

1:04:59  abstract process and turn them into language. And once that thinking has been done, then it's just there. It's

1:05:05  available. It's on the surface and you just nick it. Um Lauren, thank you so much. This has been glorious.

1:05:11  Yeah, this has been super fun. I really enjoyed talking to you. Hope we can do it again. I'd love to do it again. I'd

1:05:19  love to do it again. Absolutely. Um yeah, we'll check in in uh I don't know. Yeah, Monday. Let's do it.