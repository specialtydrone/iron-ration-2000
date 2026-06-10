---
title: "A Tale of Sim Cities"
written: 2023-03-19
published: 2023-03-21
type: linkedin
source: linkedin
---

*It was the best of times, it was the worst of times. It was a time of
AI-powered revolutions and of an imminent employment apocalypse for
creatives and information workers. It was a time of sorrow on Sunday
afternoon as my 16-month-old fell and bit her tongue and a time of
euphoria as I savored the end of a weekend hackathon centered on Will
Wright's 1993 masterpiece, SimCity 2000.*

**TLDR:** I spent a weekend writing a Python script that parses a
30-year-old proprietary file format and outputs 3D and 2D
representations of virtual cities with the help of GPT-4 via ChatGPT.

Despite two decades as a hobbyist programmer, this is the first project
I've felt comfortable sharing. Perhaps more importantly, I've
experienced firsthand what it's like to build something leveraging Star
Trek-level AI and I've got some thoughts about how its wider adoption
is playing out.

If any of this interests you, read on.

<img
src="https://media.licdn.com/dms/image/v2/D4E12AQFI0sSkfsr3tQ/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1679349026943?e=1782345600&amp;v=beta&amp;t=gnb1Gs5s5W3_SZxiVF9_ulh7tiYarpbWKuOTpnrdwW4"
data-media-urn="urn:li:digitalmediaAsset:D4E12AQFI0sSkfsr3tQ"
alt="No alt text provided for this image" />
<figcaption>The test city I threw together for the project.</figcaption>

## **Project Thesis**

The vintage works of Will Wright and his game studio Maxis ([rest in
peace](https://www.theverge.com/2015/3/4/8149827/ea-closing-maxis-emeryville))
captivated me as a child: SimCity 2000, SimTower, SimAnt, SimFarm,
SimIsle, etc¹. While not pushing any kind of visual boundaries at the
time compared to something like Doom, Maxis' catalog of simulations
transformed my feeble Compaq PC into a device to manage skyscrapers, ant
colonies, and pixelated cities.

It was SimCity 2000's detailed maps that captured my imagination. I
wanted to walk around those streets I'd allocated so much of my city's
budget to maintain or sail a ship through the bustling seaport I'd
developed. Maxis ultimately tried and failed to develop games to fill
this niche².

No, I wanted to create something that, if made today, would occupy the
[walking simulator
genre](https://www.salon.com/2017/11/11/a-brief-history-of-the-walking-simulator-gamings-most-detested-genre/).
Let me stroll along those tile-based boulevards and stare out at the
painfully angular terrain from the perspective of my virtual citizens
without burdensome and boring gameplay.

I've thought about implementing something like this for a long time but
last week marked the first time I saw a feasible path to implementing
it.

## Slamming Headlong into Hex Values

I felt a deep sense of dread when I opened the city's save file in HxD
for the first time. A vast ocean of unknown bytes stared back at me and
I felt completely and utterly stupid. *Perhaps*, I thought, *I'm not cut
out for this*. But my preliminary
[Google-fu](https://www.pcmag.com/encyclopedia/term/google-fu)
located fellow Maxis travelers who had solved the crux of the problem.

Two open-source projects guided my efforts: A [3D city
visualizer](https://www.youtube.com/watch?v=29wdNWRi9tY)
by the legendary [Aleksander
Krimsky](http://krimsky.net) and [unofficial
documentation](https://github.com/dfloer/SC2k-docs) of
the SimCity save file format by [Dale
Floer](https://github.com/dfloer).

Krimsky's visualizer proved less useful as it's written in C++ and I
wanted the satisfaction of implementing my own solution from scratch in
Python. Floer's documentation, on the other hand, was omnipresent for
the entirety of the project. It quickly became my Rosetta Stone.

<img
src="https://media.licdn.com/dms/image/v2/D4E12AQEZXBYNLSKDbg/article-inline_image-shrink_1500_2232/article-inline_image-shrink_1500_2232/0/1679349096655?e=1782345600&amp;v=beta&amp;t=oCR7oimnuzrbr6A5fNT2HRfr2_MU1YkGxIxTJKk3Go0"
data-media-urn="urn:li:digitalmediaAsset:D4E12AQEZXBYNLSKDbg"
alt="No alt text provided for this image" />
<figcaption>Output from my PNG renderer. You can see vegegation colored
by density, roads, buildings, and powerlines, as well as water
depth.</figcaption>

After a few hours of poking and prodding at the data, the file format
came into focus. SC2 files (a flavor of [Electronic Arts' proprietary
IFF
format](https://en.wikipedia.org/wiki/Interchange_File_Format))
utilize a very basic run-length encoding compression scheme. The
encoding is unwound with 20 lines of code dumping the data into
easily-parsed lists. Once you know the offsets into the decompressed
data for the relevant information, the rest is easy. In the end, the
stream of bytes began to resemble my test city.

[I didn't even see the code
anymore.](https://youtu.be/MvEXkd3O2ow?t=23) All I saw
were terrain heights, power lines, and roads. The data was now mine to
interpret as I pleased. I was able to export the terrain data into a
simple OBJ 3D model for use in
[Godot](https://godotengine.org/) and wrote a basic 2D
visualizer that depicts the city's features in a PNG image. Not
groundbreaking by any means, but for four evenings of work in a language
other than my native C, I'm proud of it.

<img
src="https://media.licdn.com/dms/image/v2/D4E12AQEFw7VzHBgVQw/article-inline_image-shrink_1000_1488/article-inline_image-shrink_1000_1488/0/1679346924675?e=1782345600&amp;v=beta&amp;t=g8sMLNbqM1vSEGfcKfX_IsIK-VAE-Op6-eGNV0Ih544"
data-media-urn="urn:li:digitalmediaAsset:D4E12AQEFw7VzHBgVQw"
alt="No alt text provided for this image" />
<figcaption>A smattering of my questions for ChatGPT throughout the
development.</figcaption>

## My Helpful But Lying Assistant

I've explained much of the 'why' and 'how' of this madcap project, but
what of my AI assistant? Was its [newly-released GPT-4
model](https://arstechnica.com/information-technology/2023/03/openai-checked-to-see-whether-gpt-4-could-take-over-the-world/)
able to code the entire project for me from scratch after some
exquisitely-tailored prompts?

No, it was not. Not for this project, anyway. I'm positive it would be
able to with a well-documented file format and clear instructions. After
straight-up lying to me about the dimensions of a standard SimCity 2000
map, ChatGPT was relegated to answering my questions about new-to-me
Python modules and writing 100ish lines of boilerplate code to generate
a 3D mesh based on the city's heightmap data³.

<img
src="https://media.licdn.com/dms/image/v2/D4E12AQEyDUxGpYt-2w/article-inline_image-shrink_1000_1488/article-inline_image-shrink_1000_1488/0/1679360712859?e=1782345600&amp;v=beta&amp;t=nX1O3-C6lQhFM4Z6CkZhihA1AllTGniHCE0qFHtc1Eo"
data-media-urn="urn:li:digitalmediaAsset:D4E12AQEyDUxGpYt-2w"
alt="No alt text provided for this image" />
<figcaption>Nice try, ChatGPT.</figcaption>

What struck me about working with AI is that it's simply an abbreviated
version of most software developers' workflows:

1.  Search for similar problems and their solutions
2.  Reduce the problem to a series of tasks or functions
3.  Navigate poorly-written API documentation for the tools you're
    unfamiliar with
4.  "Borrow" code snippets for solving rote problems
5.  Spend the rest of the time banging your head against the crux of the
    project

It's difficult to capture in words the feeling of at once being
thoroughly unimpressed with something while also never wanting to go
back to a world without possessing instantaneous access to so much
information on tap. It's like effortlessly finding the best parts of
Stack Overflow without the [incredibly toxic
community](https://youtu.be/I_ZK0t9-llo), pointless
gatekeeping, and soul-crushing pedantry.

Which brings me to my final thoughts.

<img
src="https://media.licdn.com/dms/image/v2/D4E12AQG_lr-eDNxCGw/article-inline_image-shrink_400_744/article-inline_image-shrink_400_744/0/1679352896001?e=1782345600&amp;v=beta&amp;t=vh7eOoIwcjqQS96qI6vTpRj_Ic7iewrkDxdh26Rr0BI"
data-media-urn="urn:li:digitalmediaAsset:D4E12AQG_lr-eDNxCGw"
alt="No alt text provided for this image" />
<figcaption>The 3D terrain map with the test city's water table rendered
in Godot.</figcaption>

## A Reckoning for Careers Built on Cruft

In my *A Tale of Two Cities*-inspired introduction, I referenced an
impending apocalypse for white-collar workers' career prospects. Beyond
being a fun literary allusion, I do believe a fundamental transformation
has begun among information workers and society at large.

But I'm not convinced that's an entirely bad thing.

In David Graeber's [Bullshit
Jobs](https://www.amazon.com/Bullshit-Jobs-Theory-David-Graeber/dp/150114331X),
the author documents several types of roles in organizations that only
exist to perpetuate themselves. They are jobs that are "so completely
pointless that even the person who has to perform it every day cannot
convince himself there's a good reason for him to be doing so."

In [an interview with
Vox](https://www.vox.com/2018/5/8/17308744/bullshit-jobs-book-david-graeber-occupy-wall-street-karl-marx),
the late anthropologist expounds:

> **"A lot of bullshit jobs are just manufactured middle-management
> positions with no real utility in the world, but they exist anyway in
> order to justify the careers of the people performing them. But if
> they went away tomorrow, it would make no difference at all."**

That quote deeply resonates with me. If I were a middle manager with
zero knowledge of the skills of my direct reports, an engineer whose
entire career is built on [StackOverflow
copypasta](https://stackoverflow.blog/2021/12/30/how-often-do-people-actually-copy-and-paste-from-stack-overflow-now-we-know/),
or an Upwork freelancer cranking out low-effort code for small
businesses, I'd be terrified. These people are going to lose jobs, no
question. With the [recent tech
layoffs](https://www.npr.org/2023/03/20/1164694122/amazon-is-cutting-another-9-000-jobs-as-tech-industry-keeps-shrinking),
some of them already have and it's not a stretch of the imagination to
think that large organizations like Meta and Amazon will use AI to pick
up the slack.

Like [farriers](https://en.wikipedia.org/wiki/Farrier)
after the widespread adoption of automobiles or travel agents and atlas
publishers in the wake of the internet, technological progress
eliminates entire professions and reduces others to
[novelties](https://youtu.be/eesj3pJF3lA). It's not a
good or bad thing; it simply *is.* The sooner you embrace this new
reality, the faster you can adapt to it.

Nonetheless, I believe those possessing genuine talent and the ability
to leverage AI to effectively support that talent will always be in
demand. Whether I'm one of those lucky few, I cannot yet say.

## A Time of Revolution

We're navigating a time of dramatic political upheaval and technological
revolution, not unlike the French Revolution or the rapid
industrialization of 19th-century England⁴. As you read this, fortunes
are being made and lost. Lives and livelihoods have already been
upended. But humanity has been here before and will be again.

The hard reality is that we're never going back to a time before
infinite, on-demand content generation. The bell cannot be unrung.
Regarding the times we find ourselves in, I leave you with the timeless
words of Samuel L. Jackson in Jurassic Park:

<div class="video-container">
<iframe width="560" height="315" src="https://www.youtube.com/embed/HKK4KmDlj8U?si=5anXtN6rSKAQFub2" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>

### Footnotes

1.  IMO, the canonical Maxis titles are: SimCity, SimEarth, SimAnt,
    SimLife, SimCity 2000, SimHealth, SimFarm, SimTower, SimIsle,
    SimTown, SimCopter, SimGolf, SimPark, SimTunes, Streets of SimCity,
    SimSafari, SimCity 3000, The Sims, and SimCity 4.
2.  SimCopter and Streets of SimCity attempted to make gameplay out of
    rendering the cities in 3D but they served as little more than
    static backdrops for unremarkable gameplay. Didn't stop me from
    putting many hours into SimCopter, though.
3.  If you've ever written code for generating meshes on the fly, you
    know how mind-numbing it can be. I was happy to let ChatGPT work its
    code-generating magic while I devised a way to effectively parse the
    save file.
4.  If you have any interest in understanding how humanity acts in times
    of unprecedented technological innovation and political upheaval,
    please read Eric Hobsbawm's [excellent
    book](https://www.amazon.com/Age-Revolution-1789-1848-Eric-Hobsbawm/dp/0679772537/ref=sr_1_4)
    on those subjects as he compares and contrasts them.
