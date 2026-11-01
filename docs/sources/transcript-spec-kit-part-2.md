Source: "Open Source Friday: Spec Kit Part 2", GitHub, 16 October 2026. Host Sarah Kaiser; guests Manfred and Nicole Hogan. Video: https://www.youtube.com/watch?v=8hHCpNVLhmI. Transcript pasted into the chat by Boroon on 25 October 2026. Saved verbatim as pasted.

---

0:12
Heat. Heat.
0:39
Heat. Heat.
0:45
Heat. Heat. N.
1:09
Heat. Heat.
1:17
Heat. [music]
1:39
Hey, heat. Hey, heat.
2:02
Well, welcome welcome everybody to open source Friday. Uh really excited. We have some really cool a really cool
2:09
project today. uh and some really awesome guests that I'm really I am definitely excited to talk about talk
2:15
with. Um it's also Friday, so happy Friday. Um but yeah, so quick uh point
2:24
of note, GitHub Universe is coming up. Uh my name is Sarah Kaiser. I work at
2:29
GitHub. Uh and yeah, you can check out um
2:36
the our our kind of big conference where we're announcing all kinds of new stuff um from everything from the github.com
2:43
platform to C-Pilot, all of our tooling. It's going to be super fun and you can
2:49
register for free online. So, um it's a great way to kind of stay on top of
2:55
what's going on at GitHub. All righty. So I am going to bring on
3:01
our friends for today. Um
3:07
we will be talking so we uh hey friends uh we talked about specit on a previous
3:14
episode with Manfred. Um, and so today we've got uh Manfred, who is a principal
3:20
software engineer at GitHub, as well as Nicole Hogan, who's also a principal
3:25
software [laughter] engineer at GitHub, uh, to talk about, uh, not only the 1.0
3:30
release of SpecKit, but kind of what's changed since the last time we talked. So, um, yeah, if you want to, if there's
3:37
anything else fun you want to tell folks about yourself, Manfred. Well, uh, you know, I like cats. I have
3:43
a lot of cat shirts. Let me actually show you this one. So,
3:48
uh, you know, anyway, um, yeah, still loving specit. Yes, mono, but let me let
3:55
give Nicole introduce herself. Sure, sure, sure, sure. Uh, yeah, my name is Nicole. Um, I work
4:02
remotely from Minnesota. Um, so I'm about three hours from all of America. So, just a little fun fact about myself.
4:08
Um, and like Manfred, I've been in the industry for a long time and I've been helping out with Speckit recently, which
4:13
has been really fun and interesting. So, so happy to talk more about that today. That's awesome. I didn't know that. I am
4:19
also from Minnesota originally. Are you okay? [laughter] Yep. Great. Originally from southern Minnesota and
4:24
then from the Twin Cities. So, nice. Uh, I definitely have been had had a couple birthdays at the Mall of America.
4:30
Yeah, [laughter] it's a right of passage. [clears throat] Indeed. Indeed. So, uh, yeah, let's, um,
4:38
I'm going to pull up the repo so we can chat about this, but Manfred, I'll I'll throw it to you. Um, what, uh, what's
4:47
the what's the latest and greatest on Speck? Well, as you already uh said, you know,
4:52
um, version 10 is out. Uh, you know, we're actually already at one, two, but uh,
4:58
you know, at on the birthday date, I actually uh released 10 because I thought that would be fun. You know, we
5:04
all We all turned an age well spec turned in age too you know so there we go um yeah it's been actually quite a
5:11
wild ride I mean since May uh you know we have doubled our numbers in stars
5:18
almost uh you know we doubled definitely the number ext of extensions that our
5:23
community is delivering presets are on the same way um you know yeah the star
5:28
count is going up I saw that you had the plot at the bottom of the read me earlier see that happening Um but you know
5:35
there's other things that obviously have happened that are of note and one of the things that uh you know we we've been
5:42
trying to spec it uh is to see what the community actually needs and wants. Uh
5:48
the biggest thing there is you know um if you're using it in a team you know the you know we introduced the concept
5:54
of presets for that so that you can actually layer in your own stuff but you know come you know folks were like okay
6:02
well how do I bundle this no so there you go we created bundles you know so that's one of the later editions uh so
6:09
that you can actually bundle stuff and bundling allows you to you know uh create um you know uh a vetted set of
6:18
things, valid set of extensions, valid set of presets or even workflows. Uh
6:23
yeah, I do want to call out okay we had one workflow now we have five. So
6:29
that one is finally getting off the ground as well. Uh and then previously uh you know during that era that between
6:37
you know May and now uh we were not able to actually host workflow steps which is
6:42
the steps within a workflow. Now we actually have that same hosting platform that all the other primitives has have
6:49
as well. Uh that makes it so that you know obviously can introduce your own steps because even though there are 13
6:55
core steps uh you know I don't know what kind of other steps folks would need. So you do have the ability to do that. Now
7:02
as uh Sarah's right now showing uh the other thing that happened is basically
7:07
saying you know what uh there are things that happened before SDDD and there are things that happen after SDDD. Um
7:16
SDDD is still the big is still a really big part of specit but you know we also wanted to say cater to the stage before
7:23
and that is you know how do you assess an idea? So there is a core extension
7:29
that allows you to just say hey I want to assess this idea on the merit of how does it fit the pro project and so forth
7:36
and so on. So you have the ability now to do that in same kind of guide
7:43
you know is there is this idea good meaning go is this idea bad meaning kill
7:48
or is does do I need more clarification but that's basically the end result of that process but you know the the reason
7:54
why it is there is obviously you know uh previously you would have to do a lot
8:01
more machinery and a lot of work yourself an LLM is perfectly capable of pulling all kinds of information
8:07
together if you just give it access to it. So on the far end. [laughter]
8:12
Yeah. And on the far end we obviously have bug fixing you know. So bug fixing is not normally a whole SDDD flow. Uh
8:19
you know so there you want you know hey uh assess the bug fix the bugs and then test the
8:25
bug you know test as in it did the fix actually fix the bug. So that's basically that one. And as you can see
8:32
number four is uh well create your own process you know and that is where the capability list comes in that we you
8:38
know so if Sarah scrolls down then then you can see that you know there's a lot of stuff in there that you can do uh you
8:45
know but that's all geared towards what am I trying to accomplish you know because that's the key thing really with
8:52
speckit now it's more kit than spec uh you know because [laughter] we went around of opening it up and we
8:58
wanted to see what y'all would be doing with So, having said
9:04
one second, I saw people in chat asking uh for the first episode uh to to catch
9:10
up. So, I've got a short link for you here uh if you want to open this and go back and start from the beginning,
9:17
[laughter] but because today we're we're talking about what's changed since there. But, uh yeah, you can check out the previous
9:23
uh video there. Oh, sorry. Go ahead. [laughter] The other thing that uh it's not a new
9:29
primitive, it's uh actually a addition to the core workflow and that was
9:35
convergence. uh looking at all the extensions out there uh you know we concluded that
9:41
there is there was something missing after implement and that was basically saying hey implement implemented but did
9:48
it actually adhere to the spec if it didn't convergent will actually create new tasks that implement needs to go do
9:55
to converge onto the spec which allows you then to you know make sure that
10:01
whatever was specified is actually adhered to by your implementation. So that was you know came out of obviously
10:07
all the community extensions that were around that as well and that doesn't necessarily mean that some of the
10:13
community extensions are now obsolete in that sense it's just a different way of looking at the process you know converge
10:20
does it a particular way some of the extensions in the community do it slightly different and which is that's
10:26
really the strength of specit as well it's like if you don't like it make it your own
10:32
good framework There there is one other thing and that one is highly experimental at the
10:38
moment. Um and it's also not listed in the capabilities that's why and that is
10:45
server support. So um the specket CLI can be turned into MCP mode. Uh it
10:52
slowly actually gain the [snorts] same functionality so that you can interact with it uh as part of an MCP server kind
10:59
of thing. It's not the core of what we intend to do here, but it is, you know, a way of being able to interact with the
11:05
specket CLI using MCP. So my anticipation there is not actually
11:11
running the commands through that MCP server because you know obviously the commands are still the prompts that the
11:17
agent needs to execute. So be aware of that. So I want to ask a question about the
11:24
convergence thing. Um, so that's basically trying to help make sure um
11:32
any new processes are that are generated adhere to the
11:38
previous adhere to the actual spec. Is that correct? Yeah. How does that differ from something like
11:45
having prompts or agent instructions in a repo? Uh well the the conversion command is is
11:53
is a prompt in it in in in and of it sense but it it it actually knows about the specit machinery. So the conversion
11:59
process I'm going to go look at the spec. I'm going to go look at the plan and I'm going to look at the task and
12:05
the code base and determine did I overreach? Did I underd deliver? Uh did I break
12:11
something that kind of thing in that in that particular sense. So uh the reason why it's append append only to the task
12:18
is because it needs to converge like you know it's almost like the um you know a
12:24
[snorts] loop where you go slide make that tighter and tighter and then you're actually or a funnel or how yeah that that kind
12:30
of [laughter] way right so that's asotic approach
12:37
yes um cool so now
12:43
everything that I've set obviously is core speckit and you all might wonder why Nicole is here well [clears throat]
12:52
and one of the things that I looked at speckit and you know we're at github so we have access to our co-pilot and
12:57
copilot app right so I wanted to think about hey how can I actually drive
13:03
speckit itself in actual language so that's the first uh thing that I wanted
13:08
to see because that what actually hey I don't have to remember the commands I
13:15
can just you know either chat or type uh in the in in my in my copilot app and
13:20
then you know it will just execute something. So what we did there is you know create a separate sibling
13:27
repository that is speckit copilot. Uh the reason being is is that you know the
13:33
core of copilot sorry the core of speckit stays agent agnostic as we promised. If you're on the co-pilot side
13:40
of things, you know, that particular repository will help you actually layer in uh you know, specific uh plugins,
13:48
specific specific presets that will make your uh experience in copilot better. Uh
13:54
one of them being indeed the copilot plugin that allows you to just drive
13:59
spec it completely in natural language. Uh you know, so that you don't have to remember what does this command do now.
14:06
you can just say add add this particular preset in natural language and underneath the covers the scale will
14:11
actually call co call call specit cli and then just execute it for you that was my first foray in like hey how can I
14:17
make the co-pilot experience better but then you know we started talking and uh you know Nicole and I uh uh had a lot of
14:25
fun talking about stuff and we were thinking about no well how can you actually make things visual and that's
14:31
where I will hand it off to Nicole because she did some amazing work
14:37
Quick question though. When you approach these sort of design sort of discussions
14:42
like how how long does that take? Do you sit in a room and just like write a bunch of stuff on a whiteboard? Do you use spec
14:49
kit to work on spec kit? [laughter] What what does that look like for the core of specit? Uh there are
14:56
some features I've done that. But uh remember it's an open source project. So I get a lot of PRs in you know and
15:03
obviously uh I don't know necessarily when they whether or not they use the speck it speck it to deliver it because
15:09
the PR doesn't necessarily contain that uh you know and if it does contain it I would say please scrub it because I want
15:15
to make sure that the repository stays you know uh clean in that regard because
15:21
um I view specs as uh you know uh mostly transient in that sense. I I like what
15:28
in the spec it uh repository is described as flow forward. So you've delivered something you create a new
15:34
spec for the new work. If it's that large if it's not that large then yeah I
15:39
mean you don't want to create specs if you know the change is hey I need to if
15:45
you're say for instance doing a web app hey I need to create a different color for a toggle but button that's not
15:51
really a spec right? So, um, but yeah, mostly over teams because we're both
15:56
remote and, uh, you know, we would just talk things through and, you know, uh, obviously then try things out. You know,
16:02
uh, it's a, it's a lot easier now to just say, you know what, I'm just going to give it an a day and, you know, help
16:09
throw the LLM at it and steer and guide it and see where we're at.
16:16
that uh I have definitely been throwing like I feel like when I have had a bunch
16:22
of projects that go on the like your to be red list but like to be to be done projects
16:28
uh yeah having having copilot or some other sort of LLM to just kind of cook on that in the background while I work
16:35
on other things is uh definitely pretty helpful. Uh cool. So, I'm going to we're
16:41
going to swap over to Nicole then because I'm really curious how this um
16:47
like so I full disclaimer I have used Beckit uh for basically since it
16:53
launched. I remember when it launched I was I was super excited. We were talking about it. I was telling folks about it
16:59
at conferences. Um but I haven't used it in the last couple months. So, like I'm
17:04
really excited about these kind of new I mean I I need to sit down and read through all of the cool new features and
17:12
uh capabilities but especially since I am working more with Copilot. What does it mean for
17:20
for work what does it mean to work with specit and copilot? So, I'm gonna we're
17:25
gonna share your screen Nicole. Yeah, sounds good. You can hear me?
17:32
Okay. [clears throat] Yep, we got you. Okay, perfect. Okay. Yeah, so I wanted to first just show the the spec kit
17:38
co-pilot repo that Monra talked about. Um, so if you want to learn more, I definitely encourage you to come come
17:43
check this out um and look through the readme. Uh, the key points that I want to call out here is this talks about the
17:49
five plugins that we've added um for Copilot. Uh, the first one is the one
17:54
that MRA talked about um quite a bit with that's called Speckit Copilot. And so this is what enables you to use
18:01
natural language to drive specit. And so I'm going to show that right away today. Um and then the other four are more are
18:07
more focused on um what's called a canvas app. And so uh canvas apps are a really cool feature in the GitHub
18:13
copilot app that allow you to easily create uh web apps um for really any type of UI that you want. And so we've
18:19
used that capability to provide uh really nice visual guided experiences over spec kit. So, uh, we're really
18:26
excited to, uh, to share that today. Uh, so with that, I'm going to go ahead. Sorry. Sorry.
18:33
Um, question from chat. Uh, is this only for co-pilot then?
18:39
Um, so like kind of how how can people work with speckit then with all the
18:45
options? Uh, the core of speckit is obviously agnostic. The canvases are not. The
18:50
canvases require the co-pilot app. and show us the the copilot plugin because
18:56
obviously it says copilot makes sense. Just wanted to help answer
19:02
folks questions. Yeah, no worries. Cool. Um, so yeah, I've switched to my machine. Hopefully you can see this.
19:07
Okay. Um, this is the GitHub Copilot app. Um, in case you're not familiar with it, um, it was released I want to
19:12
say in the June July time frame. Um, really it's geared towards agent first development with Copilot. And so um the
19:20
great thing that you see over here on the lefth hand side is you can open up multiple different repositories or projects which allows you to easily
19:26
switch you know in between them and have multiple different uh co-pilot sessions running um so that you can just you know
19:33
move very fluidly between different projects that you're working on. And so you can see in my lefth hand pane um I
19:39
have a couple of repos open right now. I have the speckit repo um and I I'll show that in just a moment with the canvas
19:44
apps. But the spirit behind that, right, is is that you can use speckit to actually um maintain specket. And we do that um to some degree. So those
19:51
examples will kind of help uh show that. Um and then I just have this scratch one that I'm going to start out with and
19:56
just kind of give you a feel for what the um underlying skills are that we talked about that you can use natural
20:01
language with uh to drive spec kit. Um so yeah, I already have those plugins installed here. So that's what's
20:07
enabling all the all these capabilities today. Um, but I'm going to go ahead and use the forward slash. Um, and just take
20:13
a look at some of the uh skills that are being enabled through this plugin that we talked about. Um, so there's quite a
20:19
few different uh, you know, skills or commands really uh, that you have available to you, but I'm going to just
20:24
start with the specit and one. Um, so this this allows me to initialize specit, right? And so I could use the
20:30
forward slash command. Uh, but again, just to show off the natural language, I'm just going to say, you know, initialize
20:37
my project. And I typing and uh demoing is always hard by the way, but initialize my project with
20:43
I can never type and talk at the same time. It's tough. I know. So I I'll go ahead and uh and enter that. And we'll just
20:50
give it a second here. But we should see it um load that skill here behind the scenes.
20:57
And so yeah, you can see it's loading. And so what this is doing, right, is it's setting up my project with Speckit.
21:02
And so there's certain files that Speckit uh scaffolds to basically get that ready. um as it starts to make
21:08
these changes, we'll go ahead and and look at some of those files on disk, too, just so you get a better understanding of really what's what's
21:15
being scaffolded here. Um but this should just take a few seconds to run and you can see changes are starting to
21:20
happen. So again, the the GitHub copilot app is really helpful so you can view exactly what's happening. Um so I'll
21:26
expand this and then we'll take a look at the the files on disk here. Um but before we do that, I just want to
21:31
mention here so the initialization is done and it tells us what to do next. And so, um, it basically alludes to the
21:37
fact that it actually is scaffolding more skills to help me drive K co-pilot. And so, that's why it's saying you need
21:43
to reload the skills. So, I'm going to go ahead and do that. And then the other thing it's telling me
21:48
is that I need to set up a constitution, which is typically kind of the first um step in in your spectrum and development
21:55
process so that you have your your governing principles in place. Um, so I'm going to go ahead and uh follow the
22:00
instructions there. But again, because I just reloaded my skills, I'll see some new skills that are available to me. So
22:06
I have one uh specifically for creating a constitution here. Um, again, in the
22:11
spirit of just using natural language. Um, I'm going to get rid of the forward slash and let's just uh I am going to
22:17
copy and paste some stuff because I know I know my limitations with typing and demoing. So I'm going to copy this out of a notepad I have. But uh this is
22:24
basically uh setting up my constitution. And I'm just going to give it a really really simple governing principle and
22:29
say that um for every single change I want docs and tests added. Okay. And you
22:34
know in the real world you'd have you know more principles than this but for the demo today that's what we're going to stick with. Uh so I'll go ahead and
22:41
uh press enter here and we'll just let it go. You can see here again it's inferring the underlying uh skill. And
22:47
while it's doing that um I want to take a look at the files now um that have been created. So I talked about the scaffolding that happens with spec kit.
22:53
And so, uh, when it's doing that scaffolding, it's actually creating additional skills for you to help drive
22:59
that default spec driven, um, development process workflow. Um, and so you can see here, here's that that
23:05
constitution skill that we just used. Um, and it also includes uh, skills for each of the phases for the specri
23:12
development process starting with the specification going all the way uh, through implement. Um, so these are
23:18
these are how those skills get created. Um, and then here I also want to point out, um, in the specify folder, this is
23:24
where all of the artifacts from the different, uh, pipeline phases that you run, this is where they get created. Uh,
23:29
so for example, right now we've got our, uh, constitution being created. And so I'm going to go ahead and take a look at
23:35
it and I'll open up this pane. So hopefully you can see it. Uh, but this is the constitution that it just
23:41
created. And you can see um, under the core principles that it it added what I I specified in the chat window, right?
23:47
So you have to have documentation for every change and likewise um you have to have tests. Uh so yeah so this is this
23:53
is what uh the uh spec co-pilot uh plug-in allows you to do is is to use
23:59
natural language to to drive this process. And so if you were going to keep going right you would uh then
24:05
continue on with the uh specify phase which then would uh allow you to progress through the rest of the
24:10
pipeline. Um but yeah so that's that's what I wanted to show with just the the copilot plugin. Um, the next thing is
24:16
the Canvas apps. Um, I don't know if there's any questions, but if not, I'll just kind of switch gears. Okay, pause. [laughter]
24:24
It's okay. Yes. So, we had a great question uh from
24:29
Amy here. Um, so what challenges did you run into uh like when we're so this is
24:36
obviously the the co-pilot specific piece, but how did you go about trying to kind of separate what pit what parts
24:43
should be uh agnostic or coding agent agnostic and when you're building skills
24:49
and kind of these constitutions, how do you like how how does that work
24:54
uh with the kind of broader AI landscape? Um so the core of specket always has
24:59
been agnostic. So what what it what it means is that when you're running the specify CLI to actually initialize your
25:06
project you you say I want this particular uh coding agent. So if you
25:11
have copilot you specify co-pilot if you have claude or codeex you would specify
25:16
that and it actually would generate appropriated skills for that particular
25:21
agent set. Now you can actually use multiple agents in the project but then
25:26
you just have to specify use and you have to switch between them. Um so the the key thing really is is that uh the
25:34
directory that Nicole showed where that specify is you'll notice that the
25:39
commands because that's the speckit terminology for a skill the commands are there once you actually say want to
25:46
scaffold them then they get scaffolded into the directory of your coding agent. So that way it stays completely agnostic
25:53
because when someone delivers an extension, they deliver it agnostically. When it gets installed, it would create
26:00
a skill file for that coding agent. That's super cool because then if you have uh folks on your team that are
26:07
using different coding agents, uh you still have the same kind of core instructions, uh but they kind of
26:15
translate to each different coding agent. Right. Right. Right. and and then this
26:20
particular copilot plugin actually builds on top of that. So it's actually the layer it's really nice layering that
26:26
goes, you know, up. So the copilot plugin is the is the next layer and then obviously the canvases that Nicole now
26:32
is going to show is the the layer on top of that. Okay, cool. That great question, Amy. Uh
26:40
yes. So let's uh canvases. Let's talk about canvases. I love canvases. I've been making them
26:46
like I'm pretty sure I make two to two to five canvases a day. So I [laughter] am super just uh to explain
26:54
to folks who maybe haven't tried out the the desktop app. Uh I have shared links for how to get that in uh in the
27:01
comments. I will also throw it up again one more time. Uh but basically canvases
27:06
are a way to um I mean in in some sense
27:12
they're an embedded web browser but they basically lots of apps now have this concept. I know Slack has canvases um
27:19
different kind of communication tools have them but it's just like a nice blank canvas as a way to share um you
27:27
know something more than just text from a chat or something like that. So, I tend to find myself using them to make
27:33
dashboards all the time because I'm a data science person. So, I love a good dashboard. But, uh, yeah, I'm especially
27:41
curious to see what that kind of looks like for SpecKit. So, yeah. So, we we decided to create three,
27:48
um, canvases for predefined workflows. And so, again, like I said, this is kind of an example of using spec kit to
27:54
manage spec kit because we we do do that. And these workflows are very applicable to managing spec kit. So that's why um I'm going to show these
28:01
canvases within the context of the speck kit repo. Um but yeah, so the first one I just want to start with is the
28:06
specdriven development canvas. Again, this is for like that default workflow that that spec kit provides. However, as
28:13
Manford said, you can fully uh customize uh spec kit and have the flexibility to really create whatever pipeline you
28:19
want. And then and so that's what the additional canvases will show here in just a second. Um but for the spec
28:24
driven development one, this is what a UI on top of those skills looks like. Um and so it really provides you know that
28:30
nice guided experience between different phases so that you don't necessarily have to know you know which skill to to
28:37
uh uh use next. Um you know grant granted the natural language helps but uh but this even helps even more right
28:43
if you're kind of that visual person. Um so just to walk you through the app really quickly. Um I've got some badges
28:48
here at the top that basically show you kind of different states of where um different workflow instances I've run
28:55
are at. And so I only have one workflow. That's what's in the middle here of a feature that I actually started running
29:01
through. And so that's what these counts reflect here is where I'm at. Um at the
29:06
beginning too, you can see that you can actually view your constitution. And so I already created mine. You can come in
29:11
and view that artifact if you want to. Um and if you needed, you could also create or update it. Um I am going to go
29:17
ahead and just kick off specify because I know it'll take a little bit and hopefully it'll it'll actually finish. But um I'm just going to copy and paste
29:24
a feature ID that actually comes from our community. I just picked a kind of a random issue that I saw today. Um again
29:31
using specit on specit uh and I'll go ahead and just uh hit this run specify
29:37
uh button here. And you can see in the chat window um that what's happening
29:42
here. And uh let me just go ahead. I think I might have run this before. So hopefully it doesn't cause a problem.
29:47
But um but what we should see here right is it's going to actually then invoke that specify skill um that exists
29:54
underneath to then uh basically execute this phase with the the additional prompt that I provided there with the
30:00
the feature description. And so then once I do that um it'll run the specify phase and then it'll lead me basically
30:06
through the next steps of the pipeline as needed. And so you can see here with this existing one um I ran specify um I
30:14
then went to the planning phase tasks and I I think I stopped at checklist. But if we just open one of these just to
30:20
give you a feel um I can come in here for one of these phases that already ran and I can view the artifact. So this is
30:25
my my implementation plan that got created. Just scrolling really quickly.
30:31
Um and then also uh sorry going back to the plan um you can also come in here and and rerun a phase. So if there's
30:37
additional context that you want to provide, you can certainly do that. Um but yeah, you would just kind of work your way through the phases as you
30:43
normally would, but um all using a UI to do that with. Uh so that that's what this looks like. Um the other two
30:50
canvases that I wanted to provide or an overview of really quickly is uh there's this idea assess canvas. And so uh Mford
30:58
already talked about there's these two extensions that we just added recently and this is one of those, right? So um it gives you an entirely different
31:04
pipeline than the the uh built-in spec through implementation process, right?
31:10
This is uh taking an idea and then researching it, defining, shaping, and then finally coming up with a verdict of
31:16
a a go or no-go decision. Um and so in my case, I've created a couple um of
31:22
workflow instances here where I've started to run through um those steps. Uh so for example, this one, you can see
31:28
I've actually ran through all those different phases. Um, and ultimately I I did get a decision. Um, and so if we
31:34
look at that artifact, um, it actually says that I need uh clarification. So, it didn't even give me a go or no go
31:40
decision yet. And that's because if I scroll further down, you'll see that it actually needs more context. Um, and so
31:46
this is a really another cool feature of Copilot is there's a tool underneath that allows you to ask for additional information that Copilot can do that
31:52
with. And so that's what this is leveraging. Um, so there's there's questions I need to come in here and answer and then once I submit those
31:58
answers, I can rerun the stage. Um, so yeah, that's that's kind of how the uh
32:04
the assessment pipeline works. Um, the third one Oh, yep. Did you want to say something?
32:09
Yeah, I want to make sure that people understand that this is the visualization. The actual uh commands
32:15
are run by speckit. So if you do not have the co-pilot app, you can get the
32:21
same artifacts generated by using, you know, the spec it, you know, the way you always
32:27
have. Yep, that's a good point. Um, and then the third canvas app I wanted to show is
32:34
the bug fix one. Again, uh this was another one of the extensions that Mford talked about um that basically triages a
32:41
bug um starting with the assess phase and then um assuming it's a valid bug because that's um basically kind of the
32:46
verdict that it arrives at um then you can go on to fix and actually test it within this repo. Um so again I I picked
32:54
um an actual bug from from our repository and started to run through the assessment pipeline. So that's what
33:00
we see here in the middle. Uh so if we look at the assess phase again you can view this artifact and um at the top
33:06
here you can see here's that verdict right that it's it is in fact a valid bug repo. Um so we could then go on and
33:13
and and continue with the fix and the the test phase. Um so yeah so hopefully this gives you an idea of like how you
33:19
can actually create a more guided experience um using canvases. Uh there
33:25
is a fourth canvas that I want to show you, but it's different from the the first three. Um and this is what we call
33:30
our wizard canvas. Um and the whole spirit behind this is that this is really meant to be more general purpose
33:37
and for exploration. Um so it allows you to basically peruse all the different
33:43
presets that we have available across the different cataloges. So we have a built-in catalog, we have a co-pilot
33:49
specific one, and then we also have community contributed presets. And so you can come and scroll through all of
33:55
these and choose to install them. Um likewise you can do the same thing for
34:00
extensions. And so you'll see actually I've actually installed a few. So um or actually one
34:06
one extension here, but I installed the idea assessment pipeline which is the same extension I just showed in the canvas and also the same extension that
34:13
Mra talked about. So we'll we'll show how this shows up in the the wizard. Uh but the idea here, right, is is that you
34:19
can come in and install um whatever customizations that you want to tailor
34:24
the pipeline to your scenario and your process, right? Um so with that said, I'm going to jump
34:29
to this phases tab. And this phases tab is what allows you to really build up
34:35
your pipeline and then actually execute it and try it out. Um so if you remember, like I said, I did the the
34:41
intake assessment extension. And so um this this extension has the commands
34:47
that are shown down here, right? It starts with intake. It then goes to research uh then define. I think it's
34:53
shape and then define and then decide. Um and so you can actually modify this this pipeline up here. You can remove um
35:01
different commands. Uh you can come and then add additional ones. And so what I've done here is I have added the
35:07
commands that that I'm interested in specifically for the the take pipeline. Um and at the end of this I actually
35:13
then added the specify uh phase because that's really the next step once you uh reach a verdict for your idea. Um so
35:20
again this this is just uh meant to be a tool for you to build up your pipeline visually see it and then you can come in
35:25
here and actually execute the pipeline and try out the steps. Um so I' I've already executed it but like if you look
35:32
at um I wanted to show you specify because I did run this. Uh if we view the artifact here, uh this is the actual
35:39
specs then that were created based on the original idea that I put in at the beginning of the pipeline. Uh the other
35:44
thing I'll just mention too is is I I have a fun preset installed. Manford actually created this preset, but it's called Pirate Speak. Um and so this
35:51
really shows how presets can, you know, modify your pipeline to however you want. And so this this particular preset
35:57
called Pirate Speak, uh basically outputs all of your artifacts as though it's a pirate, right? Uh uh writing it.
36:05
And so like if you look at some of the the verbiage being used here, it's it's all in the spirits of uh a pirate.
36:11
[laughter] So again, it's just really showing off, you know, the customizations that you can do um with with spec kit.
36:19
Um so yeah, so any questions about that? Because otherwise I have one more final thing I wanted to show if we have enough time. [clears throat]
36:25
Um I just want to clarify something for folks as well. when when uh Nicole
36:30
talked about the pipeline here um you know you can put things in there and take things out obviously um but the key
36:38
thing is is that those presets that uh were on the previous in the setup side that is where you can layer in your own
36:44
functionality because that's where she actually selected that pirate speak one. So you know if you have standardized
36:52
ways of working uh you know that's where you would do that and you create your own preset and then you would be able to
36:58
say hey I want to now construct my pipeline. Oh I need an particular thing that the core of speck it doesn't do.
37:04
Okay I can create an extension and then layer that into your pipeline. Yep. [snorts]
37:11
Um I'm going to uh there's a number of folks asking in chat. Yes this is uh so
37:17
specit is an open source project. Um, and a lot of the stuff that and I think pretty much everything we're showing
37:23
here in the canvases are tied to basically spec kit is underlying running
37:29
these processes and commands, right? It is. Yes.
37:35
And and the copilot specific project is also open source. So you can see how
37:40
this was done. Yeah. So even if you don't use copilot, that's totally okay. you can still
37:46
leverage everything cool about Copilot. Maybe there are cool ways to make canvases or something similar in your
37:53
favorite AI ID. Um, but that's what's awesome about uh I love good community
37:59
kind of like supported like templates or or ways that basically
38:04
folks can share how they're using a tool. Um, do you have a community page
38:10
or like a a place where people can maybe find maybe I can find it uh find all
38:15
these cool um configurations? Um, it's actually on the website of the
38:22
for the specket core, you know, it's the documentation website and then there will be a communities tab there that
38:29
folks can click on and they were they're categorized by area. So you would have one for extensions, one for presets, one
38:36
for workflows and so forth and so on. And we also have a friends page that's where folks can list their project that
38:42
uh does use specket because that's kind of the requirement but is a friend to it
38:48
folks that actually created a terminal UI for instance around specit uh you know so that's a friend of ours then.
38:55
Got it. Okay cool. Yeah, I uh I'll share some links in chat for folks and I've got the link to the main repo up right
39:02
now. Uh but yeah, I think that addresses most of the current open comments. So,
39:08
[laughter] thanks Nicole. Yeah, it was just one last thing then um that I wanted to show and this is this
39:13
is what I would say is probably extra experimental at this point. Um all the functionality that I've showed you so
39:18
far is actually checked in um to the GitHub copilot repo. So, you can access that functionality today. Um, what I'm
39:25
about to show now is not yet. Um, we're still working on it. Um, and if all goes
39:30
well, you know, we're hoping to eventually, you know, get it into the the co-pilot repo. Uh, but for now, I
39:35
just at least wanted to show you kind of where we're headed with things. Um, so again, I have the wizard open and it
39:41
looks pretty much identical to what I showed you to before. Um, however, the key differences is there's this new
39:46
button on the phases page called generate canvas. And so our idea is is is that you can build up whatever
39:53
pipeline you want, right, according to your process with the presets and extensions that you need installed. Um,
39:59
and then once you have that pipeline built up, um, you can come in here and click generate canvas and it will
40:05
actually generate that canvas app for you. Um, so you don't have to manually create it like we did. Um, and so it's
40:11
it's a, you know, great example of where you can take all this rich metadata that we're building up in wiz in the wizard and then hand it off to copilot to build
40:18
this app. And so to do this, um, the generate canvas button, um, allows you
40:24
to launch what's called the canvas designer. And I'll just go ahead and and launch that. Um, this will take a couple
40:30
of seconds, um, to do because it's actually going to create a nested session um, that we'll see here in the
40:35
lefth hand pane underneath the wizard. So that takes a little bit of time to do that. Um, and then it hands off all that
40:40
metadata that I talked about from the wizard so that it can then generate the canvas um, or get it ready for
40:47
generation. And so in the interest of time, I did go ahead and uh basically pre-launch this
40:52
canvas designer. Um we'll see a second instance probably spin up here in just a second. Um as this is working. Yeah, you
40:58
can see that there's the nested one that's creating. Um but yeah, so this is what the canvas designer would look
41:03
like. And really what it's meant to do is is that there's a couple of required fields you do need to set. So like the
41:09
canvas ID, which is the name of the file, right, for your Canvas app. Uh you also do need to provide it a title. Uh
41:14
but then I just provided a few basic FE fields um that you can use to kind of customize the generated canvas app just
41:20
a little bit more. Um so for example, you can provide a description. You can also provide like the header. Um there's
41:27
also, you know, we showed badges before. There's uh different badge rules that you can specify to have those appear. Um
41:34
and then for the appearance, there's some um general settings here, but one of the more interesting ones, right, is
41:39
being able to add your own logo, for example. And then finally, when you've just kind of finished setting up those basic settings, you can come in here and
41:46
choose to generate a canvas app. And again, it's it's based on that metadata that you've already configured in the
41:51
wizard and passes it to this, applies just these basic customizations to it, and then outputs a Canvas app for you.
41:57
And so to show you an example of one that I actually generated, um, again, this is following the bug fix assessment
42:03
pipeline that we've we've already been talking about throughout a lot today. Um, but this is what the generated app
42:08
looks like. And I I went really heavy with the badges because I was testing it out. Um but uh but yeah, you can see
42:14
these are the different badges I added through the designer. You can see my logo. You can see my custom description
42:19
that I put in uh the workflow or the the workflow header name. Um but beyond
42:25
that, you know, the behavior is just the same. It's driving spec kit underneath to call those skills that we talked about to do the bug triage where you go
42:32
through assess, bug fix, and test. And so anyway, so we thought this was really cool that you could, you know, use
42:38
Copilot to basically generate a canvas app from all that metadata from the wizard. Um, and just one more quick
42:45
thing is we also, uh, decided to make this even more customizable. Like if you
42:50
really wanted to get advanced and make your canvases even more customized to your needs, because you know, just assume those basic settings I exposed in
42:56
designer aren't enough for you. um you can actually use speckit presets presets and extensions to further customize uh
43:04
the actual app that gets generated. And so just to show you an example of that is I created a preset that takes this
43:12
horizontal display of this control and instead displays it vertically and also use autopilot mode. And so that's what
43:20
this app looks like. So it's the exact same metadata. Um, everything's the same
43:25
except I applied this this preset that changes the control layout. And so here you can see it's it's the same steps but
43:31
it's vertical and then this runs in autopilot mode. So you can just put in your um you know your bug um and let it
43:38
run. Uh so anyway just just some cool things that we've been trying um that we wanted to share. So
43:44
Oh yeah. No, I am super keen on trying this out because I
43:50
I'm a dashboard very visual person. Uh and I think it's really awesome that we have a way to Don't get me wrong, the
43:57
CLI is great. That's how I was using SpecKit before. Um that is totally
44:03
awesome and I'm actually kind of curious to check out that community project that gives it you said it's kind of like a
44:08
guey for the CLI. So I do also like those. Uh yeah. No, I think especially
44:15
with how much you can customize this like you can really make it feel like it is it is your project. These are your
44:22
workflows like um and so when you have new people come in and join you like it
44:29
I don't know it feels it feels polished. It's like when you take and actually customize a website template and so it
44:35
looks like your project's website and not just like every every other, you know, one of three basic templates for a
44:42
a generator. So that's super cool. I'm excited about that.
44:48
Um I'm going to take a look. If you have any questions for folks, uh please make sure to put them in chat. I've been
44:54
watching. Um but yeah um [clears throat]
45:01
yeah I think kind of one of the main main threads from chat is folks trying to understand which which pieces here
45:07
are copilot specific and which are not. So uh I think we've
45:13
it's relatively easy to to know uh if it's in the co in the spec co-pilot repo it's copilot specific if it's not in the
45:20
core because the core we didn't bleed it over. So the core state the core and the
45:26
copilot site is literally in that repository. Now I do want to call out for for folks that uh you know obviously
45:32
are uh interested in any of those new uh flows. Yes, you can just do the same
45:38
thing that Nicole was showing in the UI completely on the command line. The only
45:44
difference is obviously you don't get that nice UI around it. uh you know uh and yes the designer and the wizard are
45:50
not available to you because that's rarely specific to co-pilot use because it requires the canvas and the ability
45:57
then to generate the canvas and then show it you know while using copilot.
46:03
Um I I do have to say it was really interesting when we had conversations because you know asking about how we
46:09
designed this you know is something that um especially the last part that isn't
46:15
checked in yet that was really the the biggest one was like how do we how how do we think about you know you can
46:21
generate the app but then it's static. So how do how how can we layer in the same kind of concepts so that folks can
46:28
uh generate their app in their in their style you know with with their requirements that need to be there and
46:35
you know we I I asked Nicole is it possible to use presets because that it really literally was a question from me
46:41
to her and and we were like let's go yep so yeah there's the actual preset
46:47
that I created right um so that when you launch the designer you can apply that preset and then the designer installs
46:52
that basically when it's generating the canvas I okay actually probably when I explain
46:59
that the designer then runs obviously a speck it workflow to do this because otherwise wouldn't work
47:06
yep all this functionality is packaged to in its own extension actually and it's you can see that here that's it has
47:11
to be installed because that's where all of this is at and then you can override it like I said the behavior with presets
47:16
and and more extensions if you want um So, someone has raised an interesting
47:24
I I don't know if this will render nicely because it's a longer question, but I think the kind of general gist of
47:29
it is um token usage and working with spec kit.
47:35
Um are there, you know, has there been kind of any consideration about how to
47:41
be more efficient about that? Um like, you know, I I think something
47:48
that's neat about using some of these workflows is [clears throat] I don't have to go like I've made a lot
47:54
of canvases. It is quite a few tokens for me to go back and forth to change colors, change alignments of things and
48:01
being able to have presets that can I think skip a fair number of those tokens. But yeah, kind of uh how did you
48:09
go about thinking about that with the design of specit? Well, the design of speckit obviously started with at the SD the core SD
48:16
workflow. It is um um what what is SDDD for folks?
48:22
Uh spec driven development. [laughter]
48:27
That's a mouthful. Yes. Yes. Um so the core workflow obviously
48:33
uh delivers a lot of files uh because you're trying to do uh define API contracts, you're doing research, then
48:40
obviously you create your spec based on all of that. Then you have to plan it the create the implementation plan. Then
48:46
you're creating the task list that actually needs to be done. Now yes, uh one of the things once we introduced
48:53
preset it's like okay you know for a small feature that seems rather large.
48:59
So there is a preset it's called lean preset that only creates three files the spec and the task
49:05
you know yes that one consumes a whole lot less tokens but also is less uh
49:11
specified because of the fact that you don't have your API contracts there. you don't see the research, you know,
49:17
obviously the LLM did something, but it didn't actually formalize it in a file. Okay? So, it all depends on how much you
49:24
need uh and how much your organization requires of you to specify certain things out. Now, if you're talking about
49:31
a small small thing, a small feature, then yeah, use the lean preset, right?
49:36
Because it's it it it is way leaner and it's quite a quite a bit leaner actually. Now, does it come with some
49:42
certain things that you need to be aware of? Yes, it doesn't do certain things that the original core does and that's
49:50
by design. Um, but it's also an illustration of if you want to influence
49:55
how the process works, you know, you can create your own preset and say, hey, you know what? I don't want API contracts,
50:02
but I do want all the other stuff that happens. Okay, overwrite the core with a preset.
50:10
And you can do that now. And what was the secondary question? Sorry, because I kind of like
50:16
um I I think it was kind of just mostly, you know, if if you are token conscious
50:22
while you're using spec kit, what I I think you answered pretty well what the
50:29
the gist of what we're asking about. Um there was an other interesting question
50:35
uh which was um so I think the internals of spec kit are written in Python. I'm a
50:41
Pythonista. Uh I have no problem with that. But we're at kind of what was part of the design decision around uh those
50:49
sorts of architecture choices. Um I can really not answer that question because I on when Dan left our company.
50:58
So why he picked Python? Probably because he was comfortable, [laughter]
51:03
you know, and obviously you're not going to rip the you know the foundation from other people. So yeah, Python has
51:11
[snorts] I mean I think uh something I always tell people since I've used Python kind
51:17
of as my primary language for about 15 years, it's the second best language at
51:22
everything. Probably for every task like it's a Swiss Army knife. So like you know probably for any specific task
51:29
there might be a better [clears throat] more optimal choice for speed or something like that.
51:36
But whenever I need a library for something, there already is one in Python. [laughter] So [clears throat]
51:43
from the standpoint of building things, I feel like it's a and not to brag, but
51:48
it has a great community, too. So [laughter] um any any project that kind of gets to
51:55
lean into those communities, uh I think will benefit a lot. We're very friendly.
52:00
So yeah and and to point out I mean obviously when you run the actual
52:06
commands Python is not in play then it becomes that your agent that actually just reasons about the prompt it
52:12
receives and then you know whatever tooling it has you know it could be a Python tool that it calls it could be
52:18
you know a bash script it could be a PowerShell script it calls you know then it depends on what the command actually
52:23
specifies so yeah I they're fully decoupled basically
52:30
You use this to generate your specs for the specdriven development and then you
52:36
use those you know I I have definitely prior to knowing about spec sat down and
52:42
written many specification documents and unless you have like company templates
52:49
or something like that it can it's like a lot of full-time work. [laughter] So, uh, it is a great great thing to be
52:57
able to kind of start with the scaffold, uh, and then tweak as you need to. So, that [clears throat] that was why I was
53:03
originally so excited about SpecKit because I'm like, [snorts] we can have something to talk about that, you know,
53:09
is already, you know, I can turn on and off features if I don't need the API contract, stuff like that, I can just
53:15
turn those off. Um, so yeah, definitely highly suggest, especially if you are
53:21
starting new projects. um try out spec kit, see, you know, kind of see what it
53:27
helps helps you think through. Like I think it also kind of can sometimes help prompt folks to
53:33
things that they [clears throat]
53:40
that's morning um [laughter] things that folks might not be thinking through uh
53:45
kind of completely when they're designing a project. Uh I know it has definitely helped me think about oh
53:50
there's actually an interface there and I definitely need to kind of flesh out more what what are the rules around
53:56
this. So which which actually ties back into that idea assessment extension because you
54:02
know before you implement something you know uh that one actually also asked the question is it even something you should
54:09
be doing but the n [laughter] the entire process of that one is is that it actually asks you clarifying
54:16
questions. Now, you can completely ignore those obviously, but it is interesting to see those clarifying
54:22
questions because it will tell you like, did you consider this? Did you consider that? And you're like, oh, oops, I
54:28
missed something. And that's, you know, that's the thing when we're talking about an idea, it's like, did you really
54:34
think about everything that that is involved in in in what you're asking, you know, to be changed here? And that's
54:41
something that, you know, if you're working on multiple projects, it's not always an easy thing. And you know uh
54:47
yeah if you go if you if if you on board and you just have the ability to say you know what this isn't an issue that was
54:53
filed let's go see is it something that actually fits the code base or is it something that I should push back on.
55:02
Mhm. It's I feel like, and you can correct me if I'm wrong, it's like having a pocket PM [laughter]
55:09
who helps you like I've done some PM work. That's not my forte, but I do
55:14
definitely understand uh the value of having a great PM when you're working on a project. And they often are the kind
55:21
of person who asks those questions like, do we really need to be doing this now?
55:26
Um you know, have we thought about this? Uh so yeah, I think it's a really cool
55:33
structure to leverage LLMs with uh to help you work on developing your
55:39
projects. It's funny that you call pocket LLM, sorry, pocket PM, my bad. [laughter] Yes, I mean I honestly I I would
55:46
actually if you are a PM, use it. Use it. You know, you can make it your own just like the the SDDD part, you can
55:53
make it your own with your own presets for that one as well. So if you feel like okay this is this process doesn't
55:59
entirely adhere to how I would want it done you can actually uh you know tweak
56:05
it. Now obviously the commands themselves that are that you know are currently in the assessment pipeline are
56:12
uh you know there do you need to execute all of them? No. Uh but that obviously
56:17
that depends on how you actually would look at your own process which is you know uh yes we started as speckit uh you
56:24
know it really is now become a process kit [laughter]
56:29
a random I I feel like I might have to contribute this to as a community thing but I used to work on medical devices
56:35
and the software processes and requirement like you there it was like a
56:41
binder of all the things you had to check that every time somebody made a change to code like all of those rules
56:47
were followed. That feels like something that would be perfect for this. Like I'll just hand handsp spec kit this
56:53
manual and be like help me make a preset that will
56:59
when we make changes to the code actually make sure we're adhering to all of these steps. So it it's funny that
57:06
you mentioned it. Um way back where earlier in my career I actually did work
57:11
with a more regulated industry. Uh it happened to be the VA. Um they actually have what they call a
57:19
neem model. Uh that is for information interchange. Um so yes I I I I just
57:26
created the preset for it because I was like you know what let's see if I can actually do that because you know it's and and then actually see what it does.
57:32
It's very interesting to see. Now, uh I'm not trying to plug that everyone should use it or anything, but you know,
57:38
if you are interested in that, you know, go check out uh my personal repositories because that's the thing that uh I
57:44
always want to call out as well. Um I'm just as a community member as everyone else when it comes to extensions and
57:51
presets. Uh you know, we're trying things out. Uh and and obviously uh you
57:56
know because of the community and which we really love we can see what sticks and what doesn't stick because you know
58:02
the more extensions presets bundles workflows and workflow steps that that
58:07
that and canvases that come around you know the the more you know we can all help each other out.
58:14
Yeah, I that's one of the my favorite things about the open source community
58:20
is like yes, we can talk about all the cool things that this does, but you can also make it you can add new things
58:27
yourself. You can see how they work. You know, it's not just some sort of magical black box. So um when something usually
58:35
in my case I break something it gives me an opportunity to go before bugging a
58:40
bunch of people go see what what did I do wrong. [laughter] So yeah definitely uh if you are
58:47
interested in this project at all please uh go check out uh the repo for either
58:52
um we've got specit this is the main repo for the kind of coding agent agnostic pieces and basically the actual
59:00
computational backend for uh the copilot integration for specit um which
59:08
basically gives you lots of nice options in the copilot app and other copilot tooling to leverage the agnostic
59:15
So not there's not really special features or additional things. It's just
59:21
ways to make core spec kit work well in copilot. Hopefully that's an accurate
59:27
characterization. Um yeah. So I will close out um
59:35
[clears throat] with a fun question. Um what's your favorite ice cream flavor?
59:42
Pistachio. Pistachio. Okay. All right. That's a solid choice.
59:48
Mine would be cookie dough. Cookie dough. Yep. And yours? I think that's mine for Well,
59:58
nominally like a sea salt like or sea salt caramel sort of thing. However,
1:00:04
not sponsored plug [laughter] for Salt and Straw, which is like a a chain in the US. Uh, but they have a Halloween
1:00:12
flavor right now called Graveyard Cookie Crumble that is truly the best ice cream
1:00:17
flavor I have ever had. I am doing everything I can to not go there literally every day this month because
1:00:22
it rotates out at the end of the month. [laughter] I am strongly considering buying so many
1:00:28
pints and stocking my freezer with them. [laughter] But it's like really really dark chocolate with cookies in it
1:00:35
because I I do love you got to have like the kind of cookie crunch in there. Uh, and like dark like bright red white
1:00:42
chocolate swirls cuz it's a a graveyard. Anyway, [laughter]
1:00:47
uh, well, thank you so much for joining me, uh, Manford and Nicole. Yeah, thank you. You
1:00:53
um, and thanks everybody for joining us uh, online and, uh, watching the recording later. You can always catch up
1:00:59
on more Open Source Fridays. We're here pretty much every Friday. Um, I think just literally opensourcefrs.com.
1:01:06
[laughter] Um, and you can check out our whole catalog and I look forward to trying out all kinds of new spec kit
1:01:12
stuff this week and also uh what comes next for the project and hopefully some of the folks here who have uh caught up
1:01:19
in chat might be contributors to the next next iterations. That would be super cool. Just
1:01:25
thought [laughter] anyway have a good one everybody and uh we'll catch you next time.
1:01:31
