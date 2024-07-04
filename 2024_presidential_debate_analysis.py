# Pre-analysis setup pt.1: Importing necessary libraries

import nltk  # Natural Language Toolkit: used for text processing
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Pre-analysis setup pt.2: Download NLTK stopwords and tokenizer
nltk.download('punkt')
nltk.download('stopwords')

### Section 1: Defining Functions ###

def clean_text(text):
    """Clean the input text by removing stopwords and punctuation."""
    stop_words = set(stopwords.words('english'))  # Initialize stopwords from NLTK
    #  Adding custom stopwords for omitting additional non-impactful words and verbs not contributing to context in the word cloud
    custom_stopwords = ["President", "president", "number", "time", "want", "wants", "lot", "look", "took", "come", "times", "could", "went",
                        "debate", "thank", "done", "Thank", "like", "going", "said", "us", "one", "back", "seen", "Well", "day", "ago",
                        "make", "sure", "never", "think", "know", "would", "fact", "things", "coming", "made", "many", "get", "got",
                        "put", "take", "thing", "see", "three", "place", "wanted", "situation", "good", "every", "much", "say", "says",
                        "guy", "even", "across", "year", "brought", "whole", "able", "way", "ever", "right", "go", "still", "half"]
    stop_words.update(custom_stopwords)

    words = word_tokenize(text)  # Tokenize the text into words
    words = [word for word in words if word.isalpha() and word.lower() not in stop_words]  # Remove punctuation and stopwords
    cleaned_text = ' '.join(words)  # Joining the cleaned words back into a single string
    
    return cleaned_text

def segregate_statements_and_export(transcript, output_file):
    """Segregate the transcript into statements by each speaker and export the cleaned statements to a text file."""
    speakers = ['TRUMP:', 'BIDEN:', 'TAPPER:', 'BASH:']  # Defining the identifiers from where to segregate the statements
    speaker_segments = {speaker: [] for speaker in speakers}  # Initialize a dictionary to store statements for each speaker

    current_speaker = None
    current_statement = []

    for line in transcript.splitlines():  # Split the transcript into lines
        for speaker in speakers:
            if line.startswith(speaker):  # To check if the line starts with a speaker identifier
                if current_speaker:
                    cleaned_statement = clean_text(' '.join(current_statement))  # Clean the current statement
                    speaker_segments[current_speaker].append(cleaned_statement)  # Save the cleaned statement
                    current_statement = []  # Reset current statement list
                
                current_speaker = speaker  # Set current speaker
                current_statement.append(line[len(speaker):].strip())
                break
        else:
            current_statement.append(line.strip())
    
    if current_speaker and current_statement:
        cleaned_statement = clean_text(' '.join(current_statement))  # Clean the last speaker's statement
        speaker_segments[current_speaker].append(cleaned_statement)  # Save the cleaned statement

    with open(output_file, 'w', encoding='utf-8') as f:
        for speaker, statements in speaker_segments.items():
            f.write(f"{speaker} cleaned statements:\n")
            for statement in statements:
                f.write(f"- {statement}\n")
            f.write("\n")
    
    print(f"Cleaned transcript exported to '{output_file}'")
    
    return speaker_segments

def word_frequency_analysis(speaker_statements):
    """Perform word frequency analysis on the cleaned statements of a speaker."""
    all_words = []
    for statement in speaker_statements:
        words = statement.split()  # Split statement into words
        all_words.extend(words)  # Add words to the list

    word_counts = Counter(all_words)  # Counting word frequencies
    
    return word_counts  # Return word counts

def plot_word_cloud(word_counts, speaker):
    """Generate and plot a word cloud based on word frequencies for a given speaker."""
    wordcloud = WordCloud(width=1000, height=800, background_color='Black').generate_from_frequencies(word_counts)  # Generate a word cloud

    plt.figure(figsize=(15, 8))  # Set figure size
    plt.imshow(wordcloud, interpolation='bilinear')  # Display the word cloud
    plt.title(f"Word Cloud for {speaker}")  # Set title
    plt.axis('off')  # Hide axis
    plt.show()  # Show the plot

### Section 2: Processing the Transcript ###

# I have pasted the entire debate transcript (96000+ characters) from the official source (CNN) below for my convenience;
# An alternate way would be to store the transcript in a .txt file and source it from the project directory, in which case the code would need changes
# Second half of the code continues after the transcript below
transcript = """
CNN — 
President Joe Biden and former President Donald Trump participated in their first debate of the 2024 election season on CNN in Atlanta Thursday.
Read the final, corrected transcript of the debate below:
JAKE TAPPER, CNN MODERATOR: We’re live from Georgia, a key battleground state in the race for the White House. In just moments, the current U.S. president will debate the former U.S. president as their parties’ presumptive nominees, a first in American history.
We want to welcome our viewers in the United States and around the world to our studios in Atlanta.
This is the CNN presidential debate.
DANA BASH, CNN MODERATOR: This debate is being produced by CNN and it’s coming to you live on CNN, CNN International, CNN.com, CNN Max, and CNN Espanol.
This is a pivotal moment between President Joe Biden and former President Donald Trump in their rematch for the nation’s highest office. Each will make his case to the American people with just over four months until Election Day.
Good evening. I’m Dana Bash, anchor of CNN’s “Inside Politics” and co-anchor of “State Of The Union.”
TAPPER:  I’m Jake Tapper, anchor of CNN’s “The Lead” and co-anchor of “State Of The Union.”
Dana and I will co-moderate this evening. Our job is to facilitate a debate between the two candidates tonight.
Before we introduce them, we want to share the rules of the debate with the audience at home.
Former President Trump will be on the left side of the screen. President Biden will be appearing on the right. A coin toss determined their positions.
Each candidate will have two minutes to answer a question, and one minute each for responses and rebuttals. An additional minute for follow-up, clarification or response is at the moderators’ discretion.
BASH:  When it’s time for a candidate to speak, his microphone will be turned on and his opponent’s microphone will be turned off. Should a candidate interrupt when his microphone is muted, he will be difficult to understand for viewers at home.
At the end of the debate, each candidate will get two minutes for closing statements.
There is no studio audience tonight. Pre-written notes, props or contact with campaign staff are not permitted during the debate.
By accepting our invitation to debate, both candidates and their campaigns agreed to accept these rules.
TAPPER:  Now please welcome the 46th president of the United States, Joe Biden.
JOE BIDEN, PRESIDENT OF THE UNITED STATES: How are you? Good to be here. Thank you.
TAPPER:  And please welcome the 45th president of the United States, Donald Trump.
Gentlemen, thanks so much for being here. Let’s begin the debate. And let’s start with the issue that voters consistently say is their top concern, the economy.
President Biden, inflation has slowed, but prices remain high. Since you took office, the price of essentials has increased. For example, a basket of groceries that cost $100 then, now costs more than $12; and typical home prices have jumped more than 30 percent.
What do you say to voters who feel they are worse off under your presidency than they were under President Trump?
BIDEN:  You have to take a look at what I was left when I became president, what Mr. Trump left me.
We had an economy that was in freefall. The pandemic are so badly handled, many people were dying. All he said was, it’s not that serious. Just inject a little bleach in your arm. It’d be all right.
The economy collapsed. There were no jobs. Unemployment rate rose to 15 percent. It was terrible.
And so, what we had to do is try to put things back together again. That’s exactly what we began to do. We created 15,000 new jobs. We brought on – in a position where we have 800,000 new manufacturing jobs.
But there’s more to be done. There’s more to be done. Working class people are still in trouble.
I come from Scranton, Pennsylvania. I come from a household where the kitchen table – if things weren’t able to be met during the month was a problem. Price of eggs, the price of gas, the price of housing, the price of a whole range of things.
That’s why I’m working so hard to make sure I deal with those problems. And we’re going to make sure that we reduce the price of housing. We’re going to make sure we build 2 million new units. We’re going to make sure we cap rents, so corporate greed can’t take over.
The combination of what I was left and then corporate greed are the reason why we’re in this problem right now.
In addition to that, we’re in a situation where if you had – take a look at all that was done in his administration, he didn’t do much at all. By the time he left, there’s – things had been in chaos. There was (ph) literally chaos.
And so, we put things back together. We created, as I said, those (ph) jobs. We made sure we had a situation where we now – we brought down the price of prescription drugs, which is a major issue for many people, to $15 for – for an insulin shot, as opposed to $400. No senior has to pay more than $200 for any drug – all the drugs they (inaudible) beginning next year.
And the situation is making – and we’re going to make that available to everybody, to all Americans. So we’re working to bring down the prices around the kitchen table. And that’s what we’re going to get done.
TAPPER:  Thank you.
President Trump?
DONALD TRUMP, FORMER PRESIDENT OF THE UNITED STATES AND CURRENT U.S. PRESIDENTIAL CANDIDATE: We had the greatest economy in the history of our country. We had never done so well. Every – everybody was amazed by it. Other countries were copying us.
We got hit with COVID. And when we did, we spent the money necessary so we wouldn’t end up in a Great Depression the likes of which we had in 1929. By the time we finished – so we did a great job. We got a lot of credit for the economy, a lot of credit for the military, and no wars and so many other things. Everything was rocking good.
But the thing we never got the credit for, and we should have, is getting us out of that COVID mess. He created mandates; that was a disaster for our country.
But other than that, we had – we had given them back a – a country where the stock market actually was higher than pre-COVID, and nobody thought that was even possible. The only jobs he created are for illegal immigrants and bounceback jobs; they’re bounced back from the COVID.
He has not done a good job. He’s done a poor job. And inflation’s killing our country. It is absolutely killing us.
TAPPER:  Thank you.
President Biden?
BIDEN:  Well, look, the greatest economy in the world, he’s the only one who thinks that, I think. I don’t know anybody else who thinks it was great – he had the greatest economy in the world.
And, you know, the fact of the matter is that we found ourselves in a situation where his economy – he rewarded the wealthy. He had the largest tax cut in American history, $2 trillion. He raised the deficit larger than any president has in any one term. He’s the only president other than Herbert Hoover who has lost more jobs than he had when he began, since Herbert Hoover. The idea that he did something that was significant.
And the military – you know, when he was president, they were still killing people in Afghanistan. He didn’t do anything about that. When he was president, we still found ourselves in a position where you had a notion that we were this safe country. The truth is, I’m the only president this century that doesn’t have any – this – this decade – doesn’t have any troops dying anywhere in the world, like he did.
TAPPER:  President Trump, I want to follow up, if I can. You wanted…
TRUMP:  Am I allowed to respond to him?
TAPPER:  Well, I’m going to ask you a follow-up. You can do whatever you want with the minute that we give you.
I want to follow up. You want to impose a 10 percent tariff on all goods coming into the U.S. How will you ensure that that doesn’t drive prices even higher?
TRUMP:  Not going to drive them higher. It’s just going to cause countries that have been ripping us off for years, like China and many others, in all fairness to China – it’s going to just force them to pay us a lot of money, reduce our deficit tremendously, and give us a lot of power for other things.
But he – he made a statement. The only thing he was right about is I gave you the largest tax cut in history. I also gave you the largest regulation cut in history. That’s why we had all the jobs. And the jobs went down and then they bounced back and he’s taking credit for bounceback jobs. You can’t do that.
He also said he inherited 9 percent inflation. No, he inherited almost no inflation and it stayed that way for 14 months. And then it blew up under his leadership, because they spent money like a bunch of people that didn’t know what they were doing. And they don’t know what they were doing. It was the worst – probably the worst administration in history. There’s never been.
And as far as Afghanistan is concerned, I was getting out of Afghanistan, but we were getting out with dignity, with strength, with power. He got out, it was the most embarrassing day in the history of our country’s life.
TAPPER:  President Trump, over the last eight years, under both of your administrations, the national debt soared to record highs. And according to a new non-partisan analysis, President Trump, your administration approved $8.4 trillion in new debt. While so far, President Biden, you’ve approved $4.3 trillion in new debt.
So former President Trump, many of the tax cuts that you signed into law are set to expire next year. You want to extend them and go even further, you say. With the U.S. facing trillion-dollar deficits and record debt, why should top earners and corporations pay even less in taxes than they do now?
TRUMP:  Because the tax cuts spurred the greatest economy that we’ve ever seen just prior to COVID, and even after COVID. It was so strong that we were able to get through COVID much better than just about any other country. But we spurred – that tax spurred.
Now, when we cut the taxes – as an example, the corporate tax was cut down to 21 percent from 39 percent, plus beyond that – we took in more revenue with much less tax and companies were bringing back trillions of dollars back into our country.
The country was going like never before. And we were ready to start paying down debt. We were ready to start using the liquid gold right under our feet, the oil and gas right under our feet. We were going to have something that nobody else has had. We got hit with COVID. We did a lot to fix it. I gave him an unbelievable situation, with all of the therapeutics and all of the things that we came up with. We – we gave him something great.
Remember, more people died under his administration, even though we had largely fixed it. More people died under his administration than our administration, and we were right in the middle of it. Something which a lot of people don’t like to talk about, but he had far more people dying in his administration.
He did the mandate, which is a disaster. Mandating it. The vaccine went out. He did a mandate on the vaccine, which is the thing that people most objected to about the vaccine. And he did a very poor job, just a very poor job.
And I will tell you, not only poor there, but throughout the entire world, we’re no longer respected as a country. They don’t respect our leadership. They don’t respect the United States anymore.
We’re like a Third World nation. Between weaponization of his election, trying to go after his political opponent, all of the things he’s done, we’ve become like a Third World nation. And it’s a shame the damage he’s done to our country.
And I’d love to ask him, and will, why he allowed millions of people to come in here from prisons, jails and mental institutions to come into our country and destroy our country.
TAPPER:  President Trump, we will get to immigration later in this block.
President Biden, I want to give you an opportunity to respond to this question about the national debt.
BIDEN:  He had the largest national debt of any president four-year period, number one.
Number two, he got $2 trillion tax cut, benefited the very wealthy.
What I’m going to do is fix the taxes.
For example, we have a thousand trillionaires in America – I mean, billionaires in America. And what’s happening? They’re in a situation where they, in fact, pay 8.2 percent in taxes. If they just paid 24 percent or 25 percent, either one of those numbers, they’d raised $500 million – billion dollars, I should say, in a 10-year period.
We’d be able to right – wipe out his debt. We’d be able to help make sure that – all those things we need to do, childcare, elder care, making sure that we continue to strengthen our healthcare system, making sure that we’re able to make every single solitary person eligible for what I’ve been able to do with the COVID – excuse me, with dealing with everything we have to do with.
Look, if – we finally beat Medicare.
TAPPER:  Thank you, President Biden.
President Trump?
TRUMP:  Well, he’s right: He did beat Medicaid (ph). He beat it to death. And he’s destroying Medicare, because all of these people are coming in, they’re putting them on Medicare, they’re putting them on Social Security. They’re going to destroy Social Security.
This man is going to single-handedly destroy Social Security. These millions and millions of people coming in, they’re trying to put them on Social Security. He will wipe out Social Security. He will wipe out Medicare. So he was right in the way he finished that sentence, and it’s a shame.
What’s happened to our country in the last four years is not to be believed. Foreign countries – I’m friends with a lot of people. They cannot believe what happened to the United States of America. We’re no longer respected. They don’t like us. We give them everything they want, and they – they think we’re stupid. They think we’re very stupid people.
What we’re doing for other countries, and they do nothing for us. What this man has done is absolutely criminal.
TAPPER:  Thank you, President Trump.
Dana?
BASH:  This is the first presidential election since the Supreme Court overturned Roe v. Wade. This morning, the court ruled on yet another abortion case, temporarily allowing emergency abortions to continue in Idaho despite that state’s restrictive ban.
Former President Trump, you take credit for the decision to overturn Roe v. Wade, which returned the issue of abortion to the states.
TRUMP:  Correct.
BASH:  However, the federal government still plays a role in whether or not women have access to abortion pills. They’re used in about two-thirds of all abortions.
As president, would you block abortion medication?
TRUMP:  First of all, the Supreme Court just approved the abortion pill. And I agree with their decision to have done that, and I will not block it.
And if you look at this whole question that you’re asking, a complex, but not really complex – 51 years ago, you had Roe v. Wade, and everybody wanted to get it back to the states, everybody, without exception. Democrats, Republicans, liberals, conservatives, everybody wanted it back. Religious leaders.
And what I did is I put three great Supreme Court justices on the court, and they happened to vote in favor of killing Roe v. Wade and moving it back to the states. This is something that everybody wanted.
Now, 10 years ago or so, they started talking about how many weeks and how many of this – getting into other things, But every legal scholar, throughout the world, the most respected, wanted it brought back to the states. I did that.
Now the states are working it out. If you look at Ohio, it was a decision that was – that was an end result that was a little bit more liberal than you would have thought. Kansas I would say the same thing. Texas is different. Florida is different. But they’re all making their own decisions right now. And right now, the states control it. That’s the vote of the people.
Like Ronald Reagan, I believe in the exceptions. I am a person that believes. And frankly, I think it’s important to believe in the exceptions. Some people – you have to follow your heart. Some people don’t believe in that. But I believe in the exceptions for rape, incest and the life of the mother. I think it’s very important. Some people don’t. Follow your heart.
But you have to get elected also and – because that has to do with other things. You got to get elected.
The problem they have is they’re radical, because they will take the life of a child in the eighth month, the ninth month, and even after birth – after birth.
If you look at the former governor of Virginia, he was willing to do this. He said, we’ll put the baby aside and we’ll determine what we do with the baby. Meaning, we’ll kill the baby.
What happened is we brought it back to the states and the country is now coming together on this issue. It’s been a great thing.
BASH:  Thank you.
President Biden?
BIDEN:  It’s been a terrible thing what you’ve done.
The fact is that the vast majority of constitutional scholars supported Roe when it was decided, supported Roe. And I was – that’s – this idea that they were all against it is just ridiculous.
And this is the guy who says the states should be able to have it. We’re in a state where in six weeks you don’t even know whether you’re pregnant or not, but you cannot see a doctor, have your – and have him decide on what your circumstances are, whether you need help.
The idea that states are able to do this is a little like saying, we’re going to turn civil rights back to the states, let each state have a different rule.
Look, there’s so many young women who have been – including a young woman who just was murdered and he went to the funeral. The idea that she was murdered by – by – by an immigrant coming in and (inaudible) talk about that.
But here’s the deal, there’s a lot of young women who are being raped by their – by their in-laws, by their – by their spouses, brothers and sisters, by – just – it’s just – it’s just ridiculous. And they can do nothing about it. And they try to arrest them when they cross state lines.
BASH:  Thank you.
TRUMP:  There have been many young women murdered by the same people he allows to come across our border. We have a border that’s the most dangerous place anywhere in the world – considered the most dangerous place anywhere in the world. And he opened it up, and these killers are coming into our country, and they are raping and killing women. And it’s a terrible thing.
As far as the abortion’s concerned, it is now back with the states. The states are voting and in many cases, they – it’s, frankly, a very liberal decision. In many cases, it’s the opposite.
But they’re voting and it’s bringing it back to the vote of the people, which is what everybody wanted, including the founders, if they knew about this issue, which frankly they didn’t, but they would have – everybody want it brought back.
Ronald Reagan wanted it brought back. He wasn’t able to get it.
Everybody wanted it brought back and many presidents had tried to get it back. I was the one to do it.
And again, this gives it the vote of the people. And that’s where they wanted it. Every legal scholar wanted it that way.
BASH:  Staying on the topic of abortion, President Biden, seven states – I’ll let you do that. This is the same topic.
Seven states have no legal restrictions on how far into a pregnancy a woman can obtain an abortion. Do you support any legal limits on how late a woman should be able to terminate a pregnancy?
BIDEN:  I supported Roe v. Wade, which had three trimesters.
First time is between a woman and a doctor. Second time is between a doctor and an extreme situation. A third time is between the doctor – I mean, it’d be between the woman and the state.
The idea that the politicians – that the founders wanted the politicians to be the ones making decisions about a woman’s health is ridiculous. That’s the last – no politician should be making that decision. A doctor should be making those decisions. That’s how it should be run. That’s what you’re going to do.
And if I’m elected, I’m going to restore Roe v. Wade.
TRUMP:  So that means he can take the life of the baby in the ninth month and even after birth, because some states, Democrat-run, take it after birth. Again, the governor – former governor of Virginia:  put the baby down, then we decide what to do with it.
So he’s in – he’s willing to, as we say, rip the baby out of the womb in the ninth month and kill the baby.
Nobody wants that to happen. Democrat or Republican, nobody wants it to happen.
BIDEN:  He’s lying. That is simply not true.
That – Roe v. Wade does not provide for that. That’s not the circumstance. Only when the woman’s life is in danger, she’s going to die, that’s the only circumstance in which that can happen.
But we are not for late-term abortion, period, period, period.
TRUMP:  Under Roe v. Wade, you have late-term abortion. You can do whatever you want. Depending on the state, you can do whatever you want.
We don’t think that’s a good thing. We think it’s a radical thing. We think the Democrats are the radicals, not the Republicans.
BIDEN:  For 51 years, that was the law. 51 years, constitutional scholarship said it was the right way to go. 51 years. And it was taken away because this guy put very conservative members on the Supreme Court. Takes credit for taking it away.
What’s he going to do? What’s he going to do, in fact, if – if the MAGA Republicans – he gets elected, and the MAGA Republicans control the Congress and they pass a universal ban on abortion, period, across the board at six weeks or seven or eight or 10 weeks, something very, very conservative? Is he going to sign that bill? I’ll veto it. He’ll sign it.
BASH:  Thank you.
TAPPER:  Let’s turn now to the issue of immigration and border security.
President Biden, a record number of migrants have illegally crossed the southern border on your watch, overwhelming border states and overburdening cities such as New York and Chicago, and in some cases causing real safety and security concerns. Given that, why should voters trust you to solve this crisis?
BIDEN:  Because we worked very hard to get a bipartisan agreement that not only changed all of that, it made sure that we are in a situation where you had no circumstance where they could come across the border with the number of border police there are now. We significantly increased the number of asylum officers. Significantly – by the way, the Border Patrol endorsed me, endorsed my position.
In addition to that, we found ourselves in a situation where, when he was president, he was taking – separating babies from their mothers, putting them in cages, making sure the families were separated. That’s not the right way to go.
What I’ve done – since I’ve changed the law, what’s happened? I’ve changed it in a way that now you’re in a situation where there are 40 percent fewer people coming across the border illegally. It’s better than when he left office. And I’m going to continue to move until we get the total ban on the – the total initiative relative to what we’re going to do with more Border Patrol and more asylum officers.
TAPPER:  President Trump?
TRUMP:  I really don’t know what he said at the end of that sentence. I don’t think he knows what he said either.
Look, we had the safest border in the history of our country. The border – all he had to do was leave it. All he had to do was leave it.
He decided to open up our border, open up our country to people that are from prisons, people that are from mental institutions, insane asylum, terrorists. We have the largest number of terrorists coming into our country right now. All terrorists, all over the world – not just in South America, all over the world. They come from the Middle East, everywhere. All over the world, they’re pouring in. And this guy just left it open.
And he didn’t need legislation because I didn’t have legislation. I said, close the border. We had the safest border in history. In that final couple of months of my presidency, we had, according to Border Patrol – who is great, and, by the way, who endorsed me for president. But I won’t say that. But they endorsed me for president.
Brandon, just speak to him.
But, look, we had the safest border in history. Now we have the worst border in history. There’s never been anything like it. And people are dying all over the place, including the people that are coming up in caravans.
TAPPER:  Thank you, President Trump.
President Biden?
BIDEN:  The only terrorist who has done anything crossing the border is one who came along and killed three in his administration, killed – an al-Qaida person in his administration killed three American soldiers, killed three American soldiers. That’s the only terrorist that’s there.
I’m not saying no terrorist ever got through. But the idea they’re emptying their prisons, we’re welcoming these people, that’s simply not true. There’s no data to support what he said.
Once again, he’s exaggerating. He’s lying.
TAPPER:  President Trump, staying on the topic of immigration, you’ve said that you’re going to carry out, quote, “the largest domestic deportation operation in American history,” unquote. Does that mean that you will deport every undocumented immigrant in America, including those who have jobs, including those whose spouses are citizens, and including those who have lived here for decades? And if so, how will you do it?
TRUMP:  Can I get one second?
He said we killed three people. The people we killed are al-Baghdadi and Salamani (sic), the two greatest terrorists, biggest terrorists anywhere in the world. And it had a huge impact on everything; not just border, on everything.
He’s the one that killed people with the bad border, including hundreds of thousands of people dying, and also killing our citizens when they come in. We – we are living right now in a rat’s nest. They’re killing our people in New York, in California, in every state in the union, because we don’t have borders anymore. Every state is now a border.
And because of his ridiculous, insane and very stupid policies, people are coming in and they’re killing our citizens at a level that we’ve never seen. We call it migrant crime. I call it Biden migrant crime.
They’re killing our citizens at a level that we’ve never seen before. And you’re reading it like these three incredible young girls over the last few days. One of them, I just spoke to the mother, and we just had the funeral for this girl, 12 years old.
This is horrible what’s taken place. What’s taken place in our country, we’re literally an uncivilized country now.
He doesn’t want it to be. He just doesn’t know. He opened the borders nobody’s ever seen anything like. And we have to get a lot of these people out and we have to get them out fast, because they’re going to destroy our country.
Just take a look at where they’re living. They’re living in luxury hotels in New York City and other places. Our veterans are on the street, they’re dying, because he doesn’t care about our veterans. He doesn’t care. He doesn’t like the military at all. And he doesn’t care about our veterans.
Nobody’s been worse. I had the highest approval rating for veterans, taking care of the V.A. He has the worst. He’s gotten rid of all the things that I approved, choice, that I got through Congress. All of the different things I approved, they abandoned.
We had, by far, the highest, and now it’s down in less than half because he’s done – all these great things that we did – and I think he did it just because I approved it, which is crazy. But he has killed so many people at our border by allowing…
TAPPER:  Thank you, President Trump.
TRUMP:  … all of these people to come in.
TAPPER:  President Biden…
TRUMP:  And it’s a very sad day in America.
TAPPER:  President Biden, you have the mic.
BIDEN:  Every single thing he said is a lie, every single one.
For example, veterans are a hell of a lot better off since I passed the PACT Act. One million of them now have insurance, and their families have it – and their families have it. Because what happened, whether was Agent Orange or burn pits, they’re all being covered now. And he opposed – his group opposed that.
We’re also in a situation where we have great respect for veterans. My – my son spent a year in Iraq living next to one of those burn pits. Came back with stage four glioblastoma.
I was recently in – in – in France for D-Day, and I spoke to all – about those heroes that died. I went to the World War II cemetery – World War I cemetery he refused to go to. He was standing with his four-star general, and he told him – he said, I don’t want to go in there because they’re a bunch of losers and suckers.
My son was not a loser. He was not a sucker. You’re the sucker. You’re the loser.
TAPPER:  President Trump?
TRUMP:  First of all, that was a made-up quote, suckers and losers. They made it up. It was in a third-rate magazine that’s failing, like many of these magazines. He made that up. He put it in commercials. We’ve notified them. We had 19 people that said I didn’t say it.
And think of this, who would say – I’m at a cemetery, or I’m talking about our veterans – because nobody’s taken better care – I’m so glad this came up, and he brought it up. There’s nobody that’s taken better care of our soldiers than I have.
To think that I would, in front of generals and others, say suckers and losers – we have 19 people that said it was never said by me. It was made up by him, just like Russia, Russia, Russia was made up, just like the 51 intelligence agents are made up, just like the new thing with the 16 economists are talking.
It’s the same thing. Fifty-one intelligence agents said that the laptop was Russia disinformation. It wasn’t. That came from his son Hunter. It wasn’t Russia disinformation. He made up the suckers and losers, so he should apologize to me right now.
BIDEN:  You had a four-star general stand at your side, who was on your staff, who said you said it, period. That’s number one.
And, number two, the idea – the idea that I have to apologize to you for anything along the lines. We’ve done more for veterans than any president has in American history – American history. And they now – and their family. The only sacred obligation we have as a country is to care for our veterans when they come home, and their families, and equip them when they go to war.
That’s what we’re doing. That’s what the V.A. is doing now. They’re doing more for veterans than ever before in our history.
TAPPER:  All right. Thank you so much.
BASH:  Let’s move to the topic of foreign policy. I want to begin with Russia’s war against Ukraine, which is now in its third year.
Former President Trump, Russian President Vladimir Putin says he’ll only end this war if Russia keeps the Ukrainian territory it has already claimed and Ukraine abandons its bid to join NATO.
Are Putin’s terms acceptable to you?
TRUMP:  First of all, our veterans and our soldiers can’t stand this guy. They can’t stand him. They think he’s the worst commander in chief, if that’s what you call him, that we’ve ever had. They can’t stand him. So let’s get that straight.
And they like me more than just about any of them. And that’s based on every single bit of information.
As far as Russia and Ukraine, if we had a real president, a president that knew – that was respected by Putin, he would have never – he would have never invaded Ukraine.
A lot of people are dead right now, much more than people know. You know, they talk about numbers. You can double those numbers, maybe triple those numbers. He did nothing to stop it. In fact, I think he encouraged Russia from going in.
I’ll tell you what happened, he was so bad with Afghanistan, it was such a horrible embarrassment, most embarrassing moment in the history of our country, that when Putin watched that and he saw the incompetence that he should – he should have fired those generals like I fired the one that you mentioned, and so he’s got no love lost. But he should have fired those generals.
No general got fired for the most embarrassing moment in the history of our country, Afghanistan, where we left billions of dollars of equipment behind, we lost 13 beautiful soldiers and 38 soldiers were obliterated. And by the way, we left people behind too. We left American citizens behind.
When Putin saw that, he said, you know what? I think we’re going to go in and maybe take my – this was his dream. I talked to him about it, his dream. The difference is he never would have invaded Ukraine. Never.
Just like Israel would have never been invaded, in a million years, by Hamas. You know why? Because Iran was broke with me. I wouldn’t let anybody do business with them. They ran out of money. They were broke. They had no money for Hamas. They had no money for anything. No money for terror.
That’s why you had no terror at all during my administration. This place, the whole world is blowing up under him.
BASH:  President Biden?
BIDEN:  I’ve never heard so much malarkey in my whole life.
Look, the fact of the matter is that we’re in a situation where – let’s take the last point first.  Iran attacked American troops, killed, caused brain damage for a number of these troops, and he did nothing about it. Recently – when he was president, they attacked. He said they’re just having headaches. That’s all it is. We didn’t do a thing when the attack took place, number one.
Number two, we got over 100,000 Americans and others out of Afghanistan during that airlift.
Number three, we found ourselves in a situation where, if you take a look at what Trump did in Ukraine, he’s – this guy told Ukraine – told Trump, do whatever you want. Do whatever you want. And that’s exactly what Trump did to Putin, encouraged him, do whatever you want. And he went in.
And listen to what he said when he went in, he was going to take Kyiv in five days, remember? Because it’s part of the old Soviet Union. That’s what he wanted to re-establish, Kyiv. And he, in fact, didn’t do it at all. He didn’t – wasn’t able to get it done. And they’ve lost over – they’ve lost thousands and thousands of troops, 500,000 troops.
BASH:  Thank you.
President Trump…
TRUMP:  I never said that.
BASH:  … I’m going to come back to you for one minute. I just want to go back to my original question, which is, are Putin’s terms acceptable to you, keeping the territory in Ukraine?
TRUMP:  No, they’re not acceptable. No, they’re not acceptable.
But look, this is a war that never should have started. If we had a leader in this war – he led everybody along. He’s given $200 billion now or more to Ukraine. He’s given $200 billion. That’s a lot of money. I don’t think there’s ever been anything like it. Every time that Zelenskyy comes to this country, he walks away with $60 billion. He’s the greatest salesman ever.
And I’m not knocking him, I’m not knocking anything. I’m only saying, the money that we’re spending on this war, and we shouldn’t be spending, it should have never happened.
I will have that war settled between Putin and Zelenskyy as president-elect before I take office on January 20th. I’ll have that war settled.
People being killed so needlessly, so stupidly, and I will get it settled and I’ll get it settled fast, before I take office.
BASH:  President Biden, you have a minute.
BIDEN:  The fact is that Putin is a war criminal. He’s killed thousands and thousands of people. And he has made one thing clear: He wants to re-establish what was part of the Soviet Empire. Not just a piece, he wants all of Ukraine. That’s what he wants.
And then do you think he’ll stop there? Do you think he’ll stop when he – if he takes Ukraine? What do you think happens to Poland? What do you think of Belarus? What do you think happens to those NATO countries?
And so, if you want a war, you ought to find out what he’s going to do. Because if, in fact, he does what he says and walks away – by the way, all that money we give Ukraine and weapons we make here in the United States. We give them the weapons, not the money at this point. And our NATO allies have produced as much funding for Ukraine as we have. That’s why it’s – that’s why we’re strong.
BASH:  Thank you.
Moving on to the Middle East, in October, Hamas attacked Israel, killing more than a thousand people and taking hundreds of hostages. Among those held and thought to still be alive are five Americans. Israel’s response has killed thousands of Palestinians and created a humanitarian crisis in Gaza.
President Biden, you’ve put forward a proposal to resolve this conflict. But so far, Hamas has not released the remaining hostages and Israel is continuing its military offensive in Gaza.
So what additional leverage will you use to get Hamas and Israel to end the war? You have two minutes.
BIDEN:  Number one, everyone from the United Nations Security Council straight through to the G7 to the Israelis and Netanyahu himself have endorsed the plan I put forward, endorsed the plan I put forward, which has three stages to it.
The first stage is trade the hostages for a ceasefire. Second phase is a ceasefire with additional conditions. The third phase is know – the end of the war.
The only one who wants the war to continue is Hamas, number one. They’re the only ones standing out (ph). We’re still pushing hard from – to get them to accept.
In the meantime, what’s happened in Israel? We’re finally – the only thing I’ve denied Israel was 2,000-pound bombs. They don’t work very well in populated areas. They kill a lot of innocent people. We are providing Israel with all the weapons they need and when they need them.
And by the way, I’m the guy that organized the world against Iran when they had a full-blown kind of ballistic – ballistic missile attack on Israel. No one was hurt. No – one Israeli was accidentally killed. And it stopped. We saved Israel.
We are the biggest producer of support for Israel than anyone in the world. And so, that’s – there’re two different things.
Hamas cannot be allowed to be continued. We continue to send our experts and our intelligence people to how they can get Hamas like we did Bin Laden. You don’t have to do it.
And by the way, they’ve been greatly weakened, Hamas, greatly weakened. And they should be. They should be eliminated.
But you got to be careful for what you use these certain weapons among population centers.
TRUMP:  Just going back to Ukraine for one second, we have an ocean separating us. The European nations together have spent $100 billion, or maybe more than that, less than us. Why doesn’t he call them so you got to put up your money like I did with NATO? I got them to put up hundreds of billions of dollars. The secretary general of NATO said Trump did the most incredible job I’ve ever seen. You wouldn’t – they wouldn’t have any – they were going out of business. We were spending – almost 100 percent of the money was – it was paid by us.
He didn’t do that. He is getting all – you got to ask these people to put up the money. We’re over $100 billion more spent, and it has a bigger impact on them, because of location, because we have an ocean in between. You got to ask them.
As far as Israel and Hamas, Israel’s the one that wants to go – he said the only one who wants to keep going is Hamas. Actually, Israel is the one. And you should them go and let them finish the job.
He doesn’t want to do it. He’s become like a Palestinian. But they don’t like him, because he’s a very bad Palestinian. He’s a weak one.
BASH:  President Biden, you have a minute.
BIDEN:  I’ve never heard so much foolishness.
This is a guy who wants to get out of NATO. You’re going to stay in NATO or you’re going to pull out of NATO?
The idea that we have – our strength lies in our alliances as well. It may be a big ocean, but we’re – (inaudible) able to avoid a war in Europe, a major war in Europe. What happens if, in fact, you have Putin continue to go into NATO? We have an Article Five agreement, attack on one is attack on all. You want to start the nuclear war he keeps talking about, go ahead, let Putin go in and control Ukraine and then move on to Poland and other places. See what happens then.
He has no idea what the hell he’s talking about.
And by the way, I got 50 other nations around the world to support Ukraine, including Japan and South Korea, because they understand that this was – this – this kind of dislocation has a serious threat to the whole world peace. No – no major war in Europe has ever been able to be contained just to Europe.
BASH:  President Trump, just to follow up, would you support the creation of an independent Palestinian state in order to achieve peace in the region?
TRUMP:  I’d have to see.
But before we do that, the problem we have is that we spend all the money. So they kill us on trade. I made great trade deals with the European nations, because if you add them up, they’re about the same size economically. Their economy is about the same size as the United States. And they were – no cars. No – they don’t want anything that we have. But we’re supposed to take their cars, their food, their everything, their agriculture. I changed that.
But the big thing I changed is they don’t want to pay. And the only reason that he can play games with NATO is because I got them to put up hundreds of billions of dollars. I said – and he’s right about this, I said, no, I’m not going to support NATO if you don’t pay. They asked me that question: Would you guard us against Russia? – at a very secret meeting of the 28 states at that time, nations at that time. And they (sic) said, no, if you don’t pay, I won’t do that. And you know what happened? Billions and billions of dollars came flowing in the next day and the next months.
But now, we’re in the same position. We’re paying everybody’s bills.
BASH:  Thank you.
TAPPER:  Let’s turn to the issue of democracy. Former President Trump, I want to ask you about January 6, 2021.
After you rallied your supporters that day, some of them stormed the Capitol to stop the constitutionally mandated counting of electoral votes. As president, you swore an oath to, quote, “preserve, protect and defend,” unquote, the Constitution. What do you say to voters who believe that you violated that oath through your actions and inaction on January 6th and worry that you’ll do it again?
TRUMP:  Well, I don’t think too many believe that.
And let me tell you about January 6th, on January 6th, we had a great border, nobody coming through, very few. On January 6th, we were energy independent. On January 6th, we had the lowest taxes ever, we had the lowest regulations ever. On January 6th, we were respected all over the world.
All over the world we were respected, and then he comes in, and we’re now laughed at, we’re like a bunch of stupid people. What happened to the United States’ reputation under this man’s leadership is horrible, including weaponization, which I’m sure at some point you’ll be talking about, where he goes after his political opponent because he can’t beat him fair and square.
TAPPER:  You have 80 seconds left. My question was: What do you say to those voters who believe that you violated your constitutional oath through your actions, inaction on January 6th, 2021, and worry that you’ll do it again?
TRUMP:  Well, I didn’t say that to anybody. I said peacefully and patriotically.
And Nancy Pelosi, if you just watch the news from two days ago, on tape to her daughter, who’s a documentary filmmaker, as they say, what she’s saying, oh, no, it’s my responsibility, I was responsible for this. Because I offered her 10,000 soldiers or National Guard, and she turned them down. And the mayor of – in writing, by the way, the mayor. In writing turned it down, the mayor of D.C. They turned it down.
I offered 10,000 because I could see – I had virtually nothing to do. They asked me to go make a speech. I could see what was happening. Everybody was saying they’re going to be there on January 6th. They’re going to be there. And I said, you know what? There’s a lot of people coming, you could feel it. You could feel it too. And you could feel it. And I said, they ought to have some National Guard or whatever. And I offered it to her. And she now admits that she turned it down. And it was the same day. She was – I don’t know, you can’t be very happy with her daughter because it made her into a liar. She said, I take full responsibility for January 6th.
TAPPER:  President Biden?
BIDEN:  Look, he encouraged those folks to go up on Capitol Hill, number one.
I sat in that dining room off the Oval Office – he sat there for three hours, three hours, watching, begging – being begged by his vice president and a number of his colleagues and Republicans as well to do something, to call for a stop, to end it. Instead, he talked – they’ve talked about these people being patriots and – and great patrons of America. In fact, he says he’ll now forgive them for what they’ve done. They’ve been convicted. He says he wants to commute their sentences and say that – no.
He went to every single court in the nation, I don’t know how many cases, scores of cases, including the Supreme Court, and they said they said – they said, no, no, this guy, this guy is responsible for doing what is being – was done.
He didn’t do a damn thing. And these people should be in jail. And they should be the ones who are being held accountable. And he wants to let them all out.
And now he says if he loses again, such a whiner that he is, that there could be a bloodbath.
TAPPER:  Thank you, President Biden.
President Trump?
TRUMP:  What they’ve done to some people that are so innocent, you ought to be ashamed of yourself, what you have done, how you’ve destroyed the lives of so many people.
When they ripped down Portland, when they ripped down many other cities – you go to Minnesota, Minneapolis, what they’ve done there with the fires all over the city. If I didn’t bring in the National Guard, that city would have been destroyed.
When you look at all of the – they took over big chunks of Seattle. I was all set to bring in the National Guard. They heard that, they saw them coming and they left immediately.
What he said about this whole subject is so off. Peacefully patriotic.
One other thing, the unselect committee, which is basically two horrible Republicans that are all gone now, out of office, and Democrats, all Democrats, they destroyed and deleted all of the information they found, because they found out we were right. We were right. And they deleted and destroyed all of the information.
They should go to jail for that. If a Republican did that, they’d go to jail.
TAPPER:  Thank you, President Trump.
President Biden, I want to give you a minute.
BIDEN:  The only person on this stage that is a convicted felon is the man I’m looking at right now. And the fact of the matter is he is – what he’s telling you is simply not true.
The fact is that there was no effort on his part to stop what was going on up on Capitol Hill. And all those people, every one of those who were convicted, deserves to be convicted. The idea that they didn’t kill somebody, just went in and broke down doors, broke the windows, occupied offices, turned over desks, turned them over, statues – the idea that those people are patriots? Come on.
When I asked him, the first of two debates we had – debates we had the first time around, I said, will you denounce the Proud Boys? He said, no, I’ll tell them to stand by. The idea he’s refusing – will you denounce these guys? Will you denounce the people we’re talking about now? Will you denounce the people who attacked that Capitol? What are you going to do?
TAPPER:  I’m going to give you a – a minute, President Trump, for a follow-up question I have.
After a jury convicted you of 34 felonies last month, you said if re-elected you would, quote, “have every right to go after,” unquote, your political opponents. You just talked about members of the Select Committee on January 6th going to jail.
Your main political opponent is standing on stage with you tonight. Can you clarify exactly what it means about you feeling you have every right to go after your political opponents?
TRUMP:  Well, I said my retribution is going to be success. We’re going to make this country successful again, because right now it’s a failing nation. My retribution’s going to be success.
But when he talks about a convicted felon, his son is a convicted felon at a very high level. His son is convicted. Going to be convicted probably numerous other times. He should have been convicted before, but his Justice Department let the statute of limitations lapse on the most important things.
But he could be a convicted felon as soon as he gets out of office. Joe could be a convicted felon with all of the things that he’s done. He’s done horrible things. All of the death caused at the border, telling the Ukrainian people that we’re going to want a billion dollars or you change the prosecutor, otherwise, you’re not getting a billion dollars.
If I ever said that, that’s quid pro quo. That – we’re not going to do anything, we’re not going to give you a billion dollars unless you change your prosecutor having to do with his son.
This man is a criminal. This man – you’re lucky. You’re lucky.
I did nothing wrong. We’d have a system that was rigged and disgusting. I did nothing wrong.
TAPPER:  Thank you, President Trump.
President Biden, you have said – I’m coming right to you, sir. You – well, you want to respond? Go ahead. I’ll give you a minute to respond.
BIDEN:  The idea that I did anything wrong relative to what you’re talking about is outrageous. It’s simply a lie, number one.
Number two, the idea that you have a right to seek retribution against any American just because you’re a president is wrong, is simply wrong. No president’s ever spoken like that before. No president in our history has spoken like that before.
Number three, the crimes that you are still charged with – and think of all the civil penalties you have. How many billions of dollars do you owe in civil penalties for molesting a woman in public, for doing a whole range of things, of having sex with a porn star on the night – and – while your wife was pregnant?
I mean, what are you talking about? You have the morals of an alley cat.
TAPPER:  Give you a minute, sir.
TRUMP:  I didn’t have sex with a porn star, number one.
Number two, that was a case that was started and moved – they moved a high-ranking official, a DOJ, into the Manhattan D.A.’s office to start that case. That case is going to be appealed in one.
We had a very terrible judge, a horrible judge, Democrat. The prosecutor were all high-ranking Democrats, appointed people. And the – both the civil and the criminal.
He basically went after his political opponent because he thought it was going to damage me. But when the public found out about these cases – because they understand it better than he does, he has no idea what these cases are. But when he – they – when they found out about these cases, you know what they did? My poll numbers went up way up. You know that because you’re reporting it. And we took in more money in the last two weeks than we’ve ever taken in in the history of any campaign, I don’t think any campaign has ever taken.
Hundreds of millions of dollars came pouring in because the public knows it’s a scam and it’s a guy that’s after his political opponent because he can’t win fair and square.
TAPPER:  Thank you, President Trump.
President Biden, you have said, quote, “Donald Trump and his MAGA Republicans are determined to destroy American democracy.”
Do you believe that the tens of millions of Americans who are likely to vote for President Trump will be voting against American democracy?
BIDEN:  The more they know about what he’s done, yes. The more they know about what he’s done.
And there’s a lot more coming. He’s got a lot of cases around the road coming around. He’s got – he’s got a whole range of issues he has to face. I don’t know what the juries will do, but I do know – I do know he has a real problem.
And so the fact that – could you ever think you’re hearing any president say that, I’m going to seek retribution? Do you ever hear any president say that he thought it might be a good idea?
What got me involved to run in the first place after my son had died, I decided – in Iraq – because of Iraq, I said, I wasn’t going to run again. Until I saw what happened in Charlottesville, Virginia, people coming out of the woods carrying swastikas on torches – torches and singing the same antisemitic bile they sang when – back in Germany.
And what did – and the young woman got killed. I spoke to the mother. And she – they asked him, they said, what – well, what do you think of those people, the people who – the one who – the ones who tried to stop it and the ones who said, I think there’s fine people on both sides?
What American president would ever say Nazis coming out of fields, carrying torches, singing the same antisemitic bile, carrying swastikas, were fine people?
This is a guy who says Hitler’s done some good things. I’d like to know what they are, the good things Hitler’s done. That’s what he said.
This guy has no sense of American democracy.
TAPPER:  President Trump?
TRUMP:  Jake, both of you know that story’s been totally wiped out. Because when you see the sentence, it said 100 percent exoneration on there. So he just keeps it going.
He says he ran because of Charlottesville. He didn’t run because of Charlottesville. He ran because it was his last chance at – he’s not equipped to be president. You know it and I know it.
It’s ridiculous. We have a debate. We’re trying to justify his presidency.
His presidency, his – without question, the worst president, the worst presidency in the history of our country. We shouldn’t be having a debate about it. There’s nothing to debate.
He made up the Charlottesville story and you’ll see it’s debunked all over the place. Every anchor has – every reasonable anchor has debunked it.
And just the other day it came out where it was fully debunked. It’s a nonsense story. He knows that.
And he didn’t run because of Charlottesville. He used that as an excuse to run.
TAPPER:  President Biden?
BIDEN:  And debunk. It happened. All you have to do is listen to what was said at the time.
And the idea that somehow that’s the only reason I ran. I ran because I was worried a guy like this guy can get elected.
If he thought they were good people coming out of that all – that forest, carrying those – those woods, carrying those torches, then he didn’t deserve to be president, didn’t deserve to be president at all.
And the idea that he’s talking about all of this being fabricated, we saw it with our own eyes. We saw what happened on January 6. We saw the people breaking through the windows. We saw people occupying there.
His own vice president – look, there’s a reason why 40 of his 44 top cabinet officers refused to endorse him this time. His vice president hasn’t endorsed him this time.
So, why? Why? They know him well. They serve with them. Why are they not endorsing him?
TAPPER:  Thank you, President Biden.
We’re going to be right back with more from the CNN presidential debate.
(COMMERCIAL BREAK)
BASH:  Welcome back to the CNN Presidential Debate live from Georgia.
Let’s talk about persistent challenges you both faced in your first terms, and you’d certainly face again in a second term. President Biden, while black unemployment dropped to a record low under your presidency, black families still earn far less than white families.
Black mothers are still three times more likely to die from pregnancy related causes. And black Americans are imprisoned at five times the rate of white Americans. What do you say to black voters who are disappointed that you haven’t made more progress?
BIDEN:  They acknowledge he made a lot of progress, number one. The facts of the matter is more small black businesses that have been started in any time in history. Number two, the wages of black – black unemployment is the lowest level it has been in a long, long time. Number three, we find them – they’re trying to provide housing for black Americans and dealing with segregation that exists among these corporate – these corporate operations that collude to keep people out of their houses.
And in addition to that, we find that the impact of, on the – the choice that black families have to make relative to childcare is incredibly difficult. When we did the first major piece of legislation in the past, I was able to reduce black childcare costs. I cut them in half, in half. We’ve got to make sure we provide for childcare costs. We’ve got to make sure – because when you provide that childcare protections, you increase economic growth because more people can be in the – in the job market.
So there’s more to be done, considerably more to be done, but we’ve done a great deal so far and I’m not letting up and they know it.
BASH:  You have 49 seconds left. What do you say to black voters who are disappointed with the progress so far?
BIDEN:  I say, I don’t blame them for being disappointed. Inflation is still hurting them badly. For example, I provided for the idea that any black family, first time home buyer should get a $10,000 tax credit to be able to buy their first home so they can get started.
I made sure that we’re in a situation where all those black families and those black individuals who provided had to take out student loans that were ballooning, that if they were engaged in nursing and anything having to do with volunteerism, if they paid their bills for 10 years on their student debt, all the rest was forgiven after 10 years. Millions have benefited from that and we’re going to do a whole lot more for black families.
BASH:  Thank you. President Trump?
TRUMP:  And he caused the inflation. He’s blaming inflation. And he’s right, it’s been very bad. He caused the inflation and it’s killing black families and Hispanic families and just about everybody. It’s killing people. They can’t buy groceries anymore. They can’t.
You look at the cost of food where it’s doubled and tripled and quadrupled. They can’t live. They’re not living anymore. He caused this inflation.
I gave him a country with no, essentially no inflation. It was perfect. It was so good. All he had to do is leave it alone. He destroyed it with his green new scam and all of the other – all this money that’s being thrown out the window.
He caused inflation. As sure as you’re sitting there, the fact is that his big kill on the black people is the millions of people that he’s allowed to come in through the border. They’re taking black jobs now and it could be 18. It could be 19 and even 20 million people. They’re taking black jobs and they’re taking Hispanic jobs and you haven’t seen it yet, but you’re going to see something that’s going to be the worst in our history.
BASH:  Thank you. President Biden?
BIDEN:  There was no inflation when I became president. You know why? The economy was flat on its back. 15 percent unemployment, he decimated the economy, absolutely decimated the economy. That’s why there was no inflation at the time.
There were no jobs. We provided thousands of millions of jobs for individuals who were involved in communities, including minority communities. We made sure that they have health insurance. We have covered with – the ACA has increased. I made sure that they’re $8,000 per person in the family to get written off in health care, but this guy wants to eliminate that. They tried 50 times. He wants to get rid of the ACA again, and they’re going to try again if they win.
You find ourselves in a position where the idea that we’re not doing it. I put more – we put more police on the street than any administration has. He wants to cut the cops. We’re providing for equity, equity, and making sure people have a shot to make it. There is a lot going on. But, on inflation, he caused it by his tremendous malfeasance in the way he handled the pandemic.
BASH:  Thank you. Another persistent challenge is the climate crisis. 2023 was the hottest year in recorded history, and communities across the country are confronting the devastating effects of extreme heat, intensifying wildfires, stronger hurricanes, and rising sea levels.
Former President Trump, you’ve vowed to end your opponent’s climate initiatives. But, will you take any action as President to slow the climate crisis?
TRUMP:  Well, let me just go back to what he said about the police, how close the police are to him. Almost every police group in the nation from every state is supporting Donald J. Trump, almost every police group. And what he has done to the black population is horrible, including the fact that for 10 years he called them super predators. We can’t, in the 1990s (ph), we can’t forget that. Super predators was his name. And he called it to them for 10, and they’ve taken great offense at it, and now they see it happening.
But, when they see what I did for criminal justice reform and for the historically black colleges and universities, where I funded them and got them all funded, and the opportunity zones with Tim. As you know, Tim Scott was - incredible, he did a great job, a great Senator from South Carolina. He came to me with the idea and it was a great idea. It’s one of the most successful economic development acts ever in the country, opportunity zones. And the biggest beneficiary are blacks. And that’s why we have the best numbers with them in maybe ever, they’re saying ever, I read this morning, wherever, the best numbers, he has lost much of the black population because he has done a horrible job for black people. He has also done a horrible job for Hispanics.
But, why do you see these millions of people pouring into our country and they’re going to take the jobs? And it’s already started. And you haven’t seen anything yet. It’s a disaster.
BASH:  38 seconds left, President Trump. Will you take any action as President to slow the climate crisis?
TRUMP:  So, I want absolutely immaculate clean water and I want absolutely clean air, and we had it. We had H2O. We had the best numbers ever. And we did – we were using all forms of energy, all forms, everything. And yet, during my four years, I had the best environmental numbers ever. And my top environmental people gave me that statistic just before I walked on the stage, actually.
BIDEN:  I don’t know where the hell he has been. The idea that, Dana, he said is true. I’ve passed the most extensive, it was the most extensive climate change legislation in history, in history. We find ourselves – and by the way, black colleges, I came up with $50 billion for HBCUs, historic black universities and colleges, because they don’t have the kind of contributors that they have to build these laboratories and the like. Any black student is capable in college in doing what any white student can do. They just have the money. But now, they’ll be able to get those jobs in high tech.
We’re in a situation where the idea that he kind of is claiming to have done something that had the cleanest water, the cleanest water? He had not done a damn thing with the environment. He – out of the Paris Peace Accord – Climate Accord, I immediately joined it, because if we reach for 1.5 degrees Celsius at any one point, well, there is no way back. The only existential threat to humanity is climate change. And he didn’t do a damn thing about it. He wants to undo all that I’ve done.
TRUMP:  The Paris Accord was going to cost us a trillion dollars, and China nothing, and Russia nothing, and India nothing. It was a ripoff of the United States. And I ended it because I didn’t want to waste that money because they treat us horribly. We were the only ones – it was costing us money. Nobody else was paying into it. And it was a disaster.
But, everything that he said just now, I’ll give you an example. I heard him say before insulin, I’m the one that got the insulin down for the seniors. I took care of the seniors. What he is doing is destroying all of our medical programs because the migrants coming in. They want everybody. And look, I have the biggest heart on the stage. I guarantee you that. And I want to take care of people. But, we’re destroying our country. They’re taking over our schools, our hospitals, and they’re going to be taking over Social Security. He is destroying Social Security, Medicare and Medicaid.
BIDEN:  Where does that come from? The idea is that we, in fact – we were the only ones of consequence or not who are not members of the Paris Accord. How can we do anything when (ph) we’re not able to – the United States can’t get it’s pollution under control? One of the largest polluters in the world, number one. We’re making significant progress. By 2035, we will have cut pollution in half. We have – we have made significant progress. And we’re continuing to make progress.
We set up a Climate Corps for thousands of young people will learn how to deal with climate, just like the Peace Corps. And we’re going to – we’re moving in directions that are going to significantly change the elements of the cause of pollution.
But the idea that he claims that he has the biggest heart up here and he’s really concerned about – about pollution and about climate, I’ve not seen any indication of that.
And, by the way, with regard to prescription drugs, one company agreed that they would reduce the price to $35, which I was calling for – one, voluntarily. I made sure every company in the world, every pharmaceutical company, cannot have to pay.
BASH:  Thank you.
BIDEN:  And, by the way…
TAPPER:  So every day millions of Americans struggle just to make ends meet. For many older Americans, Social Security provides a critical lifeline.
President Biden, if nothing is done to Social Security, seniors will see their benefits cut in just over 10 years. Will you name tonight one specific step that you’re willing to take to keep Social Security solvent?
BIDEN:  Yes, make the very wealthy begin to pay their fair share. Right now, everybody making under $170,000 pays 6 percent of their income, of their paycheck, every single time they get a paycheck, from the time of the first one they get when they’re 18 years old.
The idea that they’re going to – I’m not – I’ve been proposing that everybody, they pay – millionaires pay 1 percent – 1 percent. So no one after – I would not raise the cost of Social Security for anybody under $400,000. After that, I begin to make the wealthy begin to pay their fair share, by increasing from 1 percent beyond, to be able to guarantee the program for life.
TAPPER:  So you still have 82 seconds left. Are there any other measures that you think that would be able to help keep Social Security solvent, or is just – is that one enough?
BIDEN:  Well, that one enough will keep it solvent. But the biggest thing I’ll do, if we defeat this man, because he wants to get rid of Social Security; he thinks that there’s plenty to cut in Social Security. He’s wanting to cut Social Security and Medicare, both times. And that’s with – and if you look at the program put forward by the House Republican Caucus that he, I believe, supports, is in fact wanting to cut it as well.
The idea that we don’t need to protect our seniors is ridiculous. We put – and, by the way, the American public has greater health care coverage today than ever before. And under the ACA, as I said, you’re in a circumstance where 400,000 people – I mean, 40 million people – would not have insurance because they have a pre-existing condition. The only thing that allows them to have that insurance is the fact that they in fact are part of the ACA.
And, by the way, the other thing is we’re in a situation where I talk about education for black communities. I’ve raised the number, the amount of money for Pell grants by other $8,000 for anybody making under $70,000 a year, are going to be able to get $15,000 towards their tuition.
It’s just – he – he just doesn’t know what he’s talking about.
TAPPER:  Thank you, President Biden.
President Trump?
TRUMP:  So I’ve dealt with politicians all my life. I’ve been on this side of the equation for the last eight years. I’ve never seen anybody lie like this guy. He lies – I’ve never seen it. He could look you in the face. So – and about so many other things, too.
And we mentioned the laptop, We mentioned “Russia, Russia, Russia,” “Ukraine, Ukraine, Ukraine.” And everything he does is a lie. It’s misinformation and disinformation. The “losers and suckers” story that he made up is a total lie on the military. It’s a disgrace.
But Social Security, he’s destroying it. Because millions of people are pouring into our country, and they’re putting them on to Social Security; they’re putting them on to Medicare, Medicaid. They’re putting them in our hospitals. They’re taking the place of our citizens.
They’re – what they’re doing to the V.A., to our veterans, is unbelievable. Our veterans are living in the street and these people are living in luxury hotels. He doesn’t know what he’s doing. And it – it’s really coming back. I’ve never seen such anger in our country before.
TAPPER:  President Biden?
BIDEN:  The idea that veterans are not being taken care of, I told you before – and, by the way, when I said “suckers and losers,” he said – he acknowledged after it that he fired that general. That general got fired because he’s the one that acknowledged that that’s what he said. He was the one standing with Trump when he said it, number one.
Number two, the idea that we’re going to be in a situation where all these millions and millions, the way he talks about it, illegal aliens are coming into the country and taking away our jobs, there’s a reason why we have the fastest-growing economy in the world, a reason why we have the most successful economy in the world. We’re doing better than any other nation in the world.
And, by the way, those 15 Nobel laureates he talked about being phony, those 15 Nobel laureates, economists, they all said that, if Trump is re-elected, we’re likely to have a recession, and inflation is going to increasingly go up.
And by the way, worst president in history – 159 presidential scholars voted him the worst president in the history of the United States of America.
TAPPER:  President Biden, thank you so much. Let’s turn to the cost of childcare, which many American families struggle to afford.
President Trump, both you and President Biden have tried to address this issue, but the average cost of childcare in this country has risen to more than $11,000 a year per child. For many families, the cost of childcare for two children is more than their rent. In your second term, what would you do to make childcare more affordable?
TRUMP:  Just to go back. The general got fired because he was no good. And if he said that, that’s why he made it up. But we have 19 people that said I didn’t say it, and they’re very highly respected, much more so than him.
The other thing is, he doesn’t fire people. He never fired people. I’ve never seen him fire anybody. I did fire a lot. I fired Comey because he was no good. I fired a lot of the top people at the FBI, drained the swamp. They were no good. Not easy to fire people. You’d pay a price for it, but they were no good. I inherited these people. I didn’t put him there. I didn’t put Comey there. He was no good. I fired him.
This guy hasn’t fired anybody. He never fires. He should have fired every military man that was involved with that Afghan – the Afghanistan horror show. The most embarrassing moment in the history of our country. He didn’t fire?
Did you fire anybody? Did you fire anybody that’s on the border, that’s allowed us to have the worst border in the history of the world? Did anybody get fired for allowing 18 million people, many from prisons, many from mental institutions? Did you fire anybody that allowed our country to be destroyed? Joe, our country is being destroyed as you and I sit up here and waste a lot of time on this debate. This shouldn’t be a debate.
He is the worst president. He just said it about me because I said it. But look, he’s the worst president in the history of our country. He’s destroyed our country. Now, all of a sudden, he’s trying to get a little tough on the border. He come out – came out with a nothing deal, and it reduced it a little bit. A little bit, like this much. It’s insignificant.
He wants open borders. He wants our country to either be destroyed or he wants to pick up those people as voters. And I don’t think – we just can’t let it happen. If he wins this election, our country doesn’t have a chance. Not even a chance of coming out of this rut. We probably won’t have a country left anymore. That’s how bad it is. He is the worst in history by far.
TAPPER:  Thank you, President Trump. President Biden?
BIDEN:  We are the most admired country in the world. We’re the United States of America. There’s nothing beyond our capacity. We have the finest military in the history of the world. The finest in the history of the world. No one thinks we’re weak. No one wants to screw around with us. Nobody. Number one.
Number two, the idea that we’re talking about worst presidents. I wasn’t joking. Look it up. Go online. 159 or 58, don’t hold me to the exact number, presidential historians. They’ve had meetings and they voted who’s the worst president in American history. One through best to worst. They said he was the worst in all of American history. That’s a fact. That’s not conjecture. He can argue they are wrong, but that’s what they voted.
The idea that he is knowing (ph) – doing anything to deal with child care. He did very – virtually nothing to child care. We should significantly increase the child care tax credit. We should significantly increase the availability of women and men for child or single parents to be able to go back to work, and we should encourage businesses to hold – to have child care facilities.
TAPPER:  Thank you, President Biden. President Trump, the question was about what would you do to make child care more affordable? If you want to take your minute.
TRUMP:  Just you understand, we have polling. We have other things that do – they rate him the worst because what he’s done is so bad. And they rate me – yes, I’ll show you. I will show you. And they rate me one of the best. OK.
And if I’m given another four years, I will be the best. I think I’ll be the best. Nobody’s ever created an economy like us. Nobody ever cut taxes like us. He’s the only one I know. He wants to raise your taxes by four times. He wants to raise everybody’s taxes by four times. He wants the Trump tax cuts to expire so everybody, including the two of you are going to pay four to five times. Nobody ever heard of this before.
All my life I’d grow up and I’d see politicians talking about cutting taxes. When we cut taxes, as I said, we did more business. Apple and all these companies, they were bringing money back into our country. The worst president in history by far, and everybody knows it.
TAPPER:  President Biden?
BIDEN:  Look, the fact of the matter is that he’s dead wrong about it. He’s increased the tariff – he’s increased – he will increase the taxes on middle class people. I said I’d never raise a tax on anybody making less than $400,000. I didn’t.
But this tariff, this 10 percent tariffs. Everything coming into the country, you know what the economists say? That’s going to cost the average American $2,500 a year and more, because they’re going to have to pay the difference in food and all the things that are very important.
Number two, he’s in a situation where he talks about how he has not raised – he somehow helped the middle class. The middle class has been devastated by you. Now you want a new tax cut of $5 trillion over the next ten years, which is going to fundamentally bankrupt the country. You had the largest deficit of any president in American history, number one.
Number two, you have not, in fact, made any contact, any progress with China. We are the lowest trade deficit with China since 2010.
TAPPER:  Thank you, President Biden. Thank you, President Biden.
Let’s discuss an epidemic impacting millions of Americans that both of you have made a top priority in your first term, the opioid crisis. And for both of you, the number of overdose deaths in this country has gone up. Under your term, it went up. Under your term, it has gone up.
Former President Trump, despite the efforts that both of you have made, more than 100,000 Americans are dying from overdoses every year, primarily from fentanyl and other opioids. What will you do to help Americans right now in the throes of addiction, who are struggling to get the treatment they need?
TRUMP:  To finish up, we now have the largest deficit in the history of our country under this guy, we have the largest deficit with China. He gets paid by China. He’s a Manchurian candidate. He gets money from China. So I think he’s afraid to deal with him or something.
But do you notice? He never took out my tariffs because we bring in so much money with the tariffs that I imposed on China. He never took them away. He can’t because it’s too much money. It’s tremendous. And we saved our steel industries. And there was more to come, but he hasn’t done that.
But he hasn’t cut the tariffs because he can’t, because it’s too much money. But he’s got the largest deficit in the history of our country and he’s got the worst situation with China. China is going to own us if you keep allowing them to do what they’re doing to us as a country. They are killing us as a country, Joe, and you can’t let that happen. You’re destroying our country.
TAPPER:  So, President Trump, you have 67 seconds left. The question was, what are you going to do to help Americans in the throes of addiction right now who are struggling to get the treatment they need?
TRUMP:  Jake, we’re doing very well at addiction until the COVID came along. We had the two-and-a-half, almost three years of like nobody’s ever had before, any country in every way. And then we had to get tough. And it was – the drugs pouring across the border, we’re – it started to increase.
We got great equipment. We bought the certain dog. That’s the most incredible thing that you’ve ever seen, the way they can spot it. We did a lot. And we had – we were getting very low numbers. Very, very low numbers.
Then he came along. The numbers – have you seen the numbers now? It’s not only the 18 million people that I believe is even low, because the gotaways, they don’t even talk about gotaways. But the numbers of – the amount of drugs and human trafficking in women coming across our border, the worst thing I’ve ever seen at numbers – nobody’s ever seen under him because the border is so bad. But the number of drugs coming across our border now is the largest we’ve ever had by far.
TAPPER:  President Trump, thank you. President Biden?
BIDEN:  Fentanyl and the byproducts of fentanyl went down for a while. And I wanted to make sure we use the machinery that can detect fentanyl, these big machines that roll over everything that comes across the border, and it costs a lot of money. That was part of this deal we put together, this bipartisan deal.
More fentanyl machines, were able to detect drugs, more numbers of agents, more numbers of all the people at the border. And when we had that deal done, he went – he called his Republican colleagues said don’t do it. It’s going to hurt me politically.
He never argued it’s not a good bill. It’s a really good bill. We need those machines. We need those machines. And we’re coming down very hard in every country in Asia in terms of precursors for fentanyl. And Mexico is working with us to make sure they don’t have the technology to be able to put it together. That’s what we have to do. We need those machines.
TAPPER:  Thank you, President Biden. President Trump, and again, the question is about Americans in the throes of addiction right now struggling to get the treatment they need.
TRUMP:  Because this does pertain to it. He ended remain in Mexico, he ended catch and release. I made it catch and release in Mexico, not catch and release here. We had so many things that we had done, hard negotiations with Mexico, and I got it all for nothing.
It’s just like when you have a hostage, we always pay $6 billion for a – every time we sees hostage. Now we have a hostage. A Wall Street Journal reporter, I think a good guy, and he’s over there because Putin is laughing at this guy, probably asking for billions of dollars for the reporter.
I will have him out very quickly, as soon as I take office, before I take office. I said by literally as soon as I win the election, I will have that reporter out. He should have had him out a long time ago. But Putin is probably asking for billions and billions of dollars because this guy pays it every time.
We had two cases where we paid $6 billion for five people. I got 58 people out and I paid essentially nothing.
TAPPER:  Thank you, President Trump.
Dana.
BASH:  Let’s turn to concerns that voters have about each of you.
President Biden, you would be 86 at the end of your second term. How do you address concerns about your capability to handle the toughest job in the world well into your 80s?
BIDEN:  Well, first of all, I spent half my career being – being criticized being the youngest person in politics. I was the second-youngest person ever elected to the United States Senate. And now I’m the oldest. This guy’s three years younger and a lot less competent. I think that just look at the record. Look what I’ve done. Look how I’ve turned around the horrible situation he left me.
As I said, 50 million new jobs, 800,000 manufacturing jobs, more investment in America, over millions – billions of dollars in private investment and – and enterprises that we are growing. We’ve – by the way, we brought an awful a lot of people – the whole idea of computer chips. We used to have 40 percent of the market. We invented those chips. And we lost it because he was sending people to cheap – to find the cheapest jobs overseas and to bring home a product.
So I went – I went to South Korea. I convinced Samsung to invest billions of dollars here in the United States. And then guess what? Those fabs, they call them, to – to build these chips, those fabs pay over $100,000. You don’t need a college degree for them. And there’s billions, about $40 billion already being invested and being built right now in the United States, creating significant jobs for Americans all over – from all over the world.
BASH:  President Biden, you have 40 seconds left. Would you like to add anything?
BIDEN:  Yeah, I would. The idea that somehow we are this failing country, I never heard a president talk like this before. We – we’re the envy of the world. Name me a single major country president who wouldn’t trade places with the United States of America. For all our problems and all our opportunities, we’re the most progressive country in the world in getting things done. We’re the strongest country in the world. We’re a country in the world who keeps our word and everybody trusts us, all of our allies.
And our – those who he cuddles up to, from Kim Jong-un who he sends love letters to, or Putin, et cetera, they don’t want to screw around with us.
BASH:  Thank you.
Former President Trump, to follow up, you would be 82 at the end of your second term. What do you say to voters who have concerns about your capabilities to serve?
TRUMP:  Well, I took two tests, cognitive tests. I aced them, both of them, as you know. We made it public. He took none. I’d like to see him take one, just one, a real easy one. Like go through the first five questions, he couldn’t do it. But I took two cognitive tests. I took physical exams every year. And, you know, we knock on wood, wherever we may have wood, that I’m in very good health. I just won two club championships, not even senior, two regular club championships. To do that, you have to be quite smart and you have to be able to hit the ball a long way. And I do it. He doesn’t do it. He can’t hit a ball 50 yards. He challenged me to a golf match. He can’t hit a ball 50 yards.
I think I’m a very good shape. I feel that I’m in as good a shape as I was 25, 30 years ago. Actually, I’m probably a little bit lighter. But I’m in as good a shape as I was years ago. I feel very good. I feel the same.
But I took – I was willing to take a cognitive test. And you know what, if I didn’t do well – I aced them. Dr. Ronny Jackson, who’s a great guy, when he was White House doctor. And then I took another one, a similar one, and both – one of them said they’d never seen anybody ace them.
BASH:  Thank you.
President Biden?
BIDEN:  You’re going to see he’s six-foot-five and only 225 pounds – or 235 pounds.
TRUMP:  (inaudible).
BIDEN:  Well, you said six-four, 200.
TRUMP:  (inaudible).
BIDEN:  Well, anyway, that’s – anyway, just take a look at what he says he is and take a look at what he is.
Look, I’d be happy to have a driving contest with him. I got my handicap, which, when I was vice president, down to a 6.
And by the way, I told you before I’m happy to play golf if you carry your own bag. Think you can do it?
TRUMP:  That’s the biggest lie that he’s a 6 handicap, of all.
BIDEN:  I was 8 handicap.
TRUMP:  Yeah.
BIDEN:  Eight, but I have – you know how many…
TRUMP:  I’ve seen your swing, I know your swing.
(CROSSTALK)
BASH:  President Trump, we’re going to…
(CROSSTALK)
TRUMP:  Let’s not act like children.
BIDEN:  You are a child.
BASH:  To you, a specific concern that voters have about you. Will you pledge tonight that once all legal challenges have been exhausted that you will accept the results of this election regardless of who wins and you will say right now that political violence in any form is unacceptable?
TRUMP:  Well, I shouldn’t have to say that, but, of course, I believe that. It’s totally unacceptable.
TRUMP:  And if you would see my statements that I made on Twitter at the time, and also my statement that I made in the Rose Garden, you would say it’s one of the strongest statements you’ve ever seen.
In addition to the speech I made, in front of, I believe, the largest crowd I’ve ever spoken to, and I will tell you, nobody ever talks about that. They talk about a relatively small number of people that went to the Capitol. And in many cases were ushered in by the police.
And as Nancy Pelosi said, it was her responsibility, not mine. She said that loud and clear.
But the answer is, if the election is fair free, and I want that more than anybody.
And I’ll tell you something – I wish he was a great president because I wouldn’t be here right now. I’d be at one of my many places enjoying myself. I wouldn’t be under indictment because I wouldn’t have been his political appoint – you know, opponent. Because he indicted me because I was his opponent.
I wish he was a great president. I would rather have that.
I wouldn’t be here. I don’t mind being here, but the only reason I’m here is he’s so bad as a president that I’m going to make America great again. We’re going to make America great again.
We’re a failing nation right now. We’re a seriously failing nation. And we’re a failing nation because of him.
His policies are so bad. His military policies are insane. They’re insane.
These are wars that will never end with him. He will drive us into World War Three and we’re closer to World War Three than anybody can imagine. We are very, very close to World War Three, and he’s driving us there.
And Kim Jong-Un, and President Xi of China – Kim Jong-Un of North Korea, all of these – Putin – they don’t respect him. They don’t fear him. They have nothing going with this gentleman and he’s going to drive us into World War Three.
BIDEN:  If you want a World War Three, let him follow (ph) and win, and let Putin say, do what you want to NATO – just do what you want.
There’s a thing called Article Five, an attack on one is attack on all, a required response.
The idea – the idea – I can’t think of a single major leader in the world who wouldn’t trade places with what job I’ve done and what they’ve done because we are a powerful nation, we have wonderful piece (ph), because of the people, not me, because of the American people. They’re capable of anything and they step up when they’re needed.
And right now, we’re needed. We’re needed to protect the world because our own safety is at stake.
And again, you want to have war, just let Putin go ahead and take Kyiv, make sure they move on, see what happens in Poland, Hungary, and other places along that border. Then you have a war.
BASH:  President Trump, as I come back to you for a follow-up. The question was, will you accept the results of this election regardless of who wins?
TRUMP:  Just to finish what he said, if I might, Russia – they took a lot of land from Bush. They took a lot of land from Obama and Biden. They took no land, nothing from Trump, nothing.
He knew not to do it. He’s not going to play games with me. He knew that. I got along with him very well, but he knew not to play games.
He took nothing from me, but now, he’s going to take the whole thing from this man right here.
That’s a war that should have never started. It would’ve never started ever with me. And he’s going to take Ukraine and, you know, you asked me a question before, would you do this with – he’s got us in such a bad position right now with Ukraine and Russia because Ukraine’s not winning that war.
He said, I will never settle until such time – they’re running out of people, they’re running out of soldiers, they’ve lost so many people. It’s so sad.
They’ve lost so many people and they’ve lost those gorgeous cities with the golden domes that are 1,000-years-old, all because of him and stupid decisions.
Russia would’ve never attacked if I were president.
BASH:  President Trump, the question was, will you accept the results of the election regardless of who wins? Yes or no, please?
TRUMP:  If it’s a fair and legal and good election – absolutely. I would have much rather accepted these but the fraud and everything else was ridiculous that if you want, we’ll have a news conference on it in a week or we’ll have another one of these on – in a week.
But I will absolutely – there’s nothing I’d rather do. It would be much easier for me to do that than I’m running again. I wasn’t really going to run until I saw the horrible job he did. He’s destroying our country.
I would be very happy to be someplace else, in a nice location someplace. And again, no indictments, no political opponent’s stuff, because it’s the only way he thinks he can win.
But unfortunately, it’s driven up by numbers and driven it up to a very high level, because the people understand it.
BIDEN:  Let’s see what your numbers are when this election is over.
TRUMP:  We’ll see.
BIDEN:  Let’s see. You’re a whiner. When you lost the first time, you continued to appeal and appeal to courts all across the country.
Not one single court in America said any of your claims had any merit, state or local, none.
But you continue to promote this lie about somehow there’s all this misrepresentation, all the stealing. There’s no evidence of that at all.
And I tell you what? I doubt whether you’ll accept it because you’re such a whiner. The idea if you lose again, you’re accepting anything, you can’t stand the loss. Something snapped in you when you lost the last time.
BASH:  We’ll be right back with more from the CNN presidential debate live from Georgia.
(COMMERCIAL BREAK)
TAPPER:  It is now time for the candidates to deliver their closing statements.
As predetermined by a coin toss, we’re going to begin with you, President Biden. You have two minutes.
BIDEN:  We’ve made significant progress from the debacle that was left by President Trump in his – in his last term.
We find ourselves in a situation where, number one, we have to make sure that we have a fair tax system. I ask anyone out there in the audience, or anyone out watching this debate, do you think the tax system is fair?
The fact is that I said, nobody even making under $400,000 had a single penny increasing their taxes and it will not. And if I’m reelected, that’ll be the case again.
But this guy is – has increased your taxes because of the deficit. Number one, he’s increased inflation because of the debacle he left after – when he handled the pandemic. And he finds himself in a position where he now wants to tax you more by putting a 10 percent tariff on everything that comes into the United States America.
What I did, when, for example, he wants to get away with – and get rid of the ability of Medicare to – for the ability to – for the – us to be able to negotiate drug prices with big pharma companies.
Well, guess what? We got it – we got it down to 15 – excuse me, $35 for insulin instead of $400. No more than $2,000 for every senior no matter what they – how much prescription they need.
You know what that did? That reduced the federal deficit (ph) – debt by $160 billion over 10 years because the government doesn’t have to pay the exorbitant prices.
I’m going to make that available to every senior, all – or go longer. It’s happening now, and everybody in America. He wants to get rid of that.
We have – I’m going to make sure we have childcare. We’re going to significantly increase the credit people have for childcare. I’m going to make sure we do something about what we’re doing on lead pipes and all the things that are causing health problems for people across the country.
We’re going to continue to fight to bring down inflation and give people a break.
TAPPER:  Thank you, President Biden.
President Trump, you now have two minutes for your closing statement.
TRUMP:  Like so many politicians, this man is just a complainer. He said we want to do this. We want to do that. We want to get rid of this tax, that tax, but he doesn’t do anything. He doesn’t do.
All he does is make our country unsafe by allowing millions and millions of people to pour in. Our military doesn’t respect him. We look like fools in Afghanistan.
We didn’t stop – Israel, it was such a horrible thing that would have never happened. It should have never happened.
Iran was broke. Anybody that did business with Iran, including China, they couldn’t do business with the United States. They all passed.
Iran was broke. They had no money for Hamas or Hezbollah, for terror, no money whatsoever.
Again, Ukraine should have never happened.
He talks about all this stuff, but he didn’t do it. For three-and-a-half years, we’re living in hell. We have the Palestinians and we have everybody else rioting all over the place.
You talk about Charlottesville. This is 100 times Charlottesville, 1,000 times.
The whole country is exploding because of you, because they don’t respect you. And they have to respect their president and they don’t respect you throughout the world.
What we did was incredible. We re – rebuilt the military. We got the largest tax cut in history, the largest regulation cut in history.
The reason he’s got jobs is because I cut the regulations that gave jobs, but he’s putting a lot of those regulations back on.
All of the things that we’ve done, nobody’s ever – never seen anything like – even from a medical standpoint. Right to Try, where we can try Space Age materials instead of going to Asia or going to Europe and trying to get when you’re terminally ill.
Now, you can go and you can get something. You sign a document. They’ve been trying to get it for 42 years.
But you know what we did for the military was incredible. Choice for our soldiers, where our soldiers, instead of waiting for three months to see a doctor, can go out and get themselves fixed up and readied up, and take care of themselves and they’re living. And that’s why I had the highest approval rating of the history of the V.A.
So, all of these things – we’re in a failing nation, but it’s not going to be failing anymore. We’re going to make it great again.
BASH:  Thank you, former President Trump, President Biden.
"""

# Export and segregate statements
output_file = 'cleansed_debate_transcript.txt'  # Define the name of the output file
segregated_statements = segregate_statements_and_export(transcript, output_file)  # Segregate statements and export

# Perform word frequency analysis and plot word clouds for each speaker
for speaker, statements in segregated_statements.items():
    word_counts = word_frequency_analysis(statements)  # Perform word frequency analysis
    print(f"Word Frequencies for {speaker}:")
    for word, count in word_counts.most_common(5):  # Display top 5 words
        print(f"{word}: {count}")
    print()
    
    plot_word_cloud(word_counts, speaker)  # Plot word cloud for each speaker
