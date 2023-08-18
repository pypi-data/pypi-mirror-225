from typing import List
from llama import Type, Context, LLMEngine
import unittest

from multi_model_test import run_models, MultiModelTest


class TestBatchOperation(MultiModelTest):
    @run_models(models=["hf-internal-testing/tiny-random-gpt2"])
    def test_batch(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            favorite_song: str = Context("your favorite song")
            tone: Tone = Context("tone of the story")

        descriptors_batch = [
            Descriptors(
                likes="MANGO BARBECUE",
                favorite_song="never let me go",
                tone=Tone(tone="cheeky"),
            ),
        ] * 20 + [
            Descriptors(
                likes="llamas and other stuff",
                favorite_song="never let me go",
                tone=Tone(tone="cheeky"),
            ),
        ] * 20

        stories = self.llm(
            input=descriptors_batch,
            output_type=Story,
        )

        print(type(stories))

        print(stories)

    def test_batch_improve(self):
        class Story(Type):
            story: str = Context("the body of the story")

        class Tone(Type):
            tone: str = Context("The tone of the story")

        class Descriptors(Type):
            likes: str = Context("things you like")
            tone: Tone = Context("tone of the story")

        descriptors_batch = [
            Descriptors(
                likes="cars",
                tone=Tone(tone="happy"),
            ),
            Descriptors(
                likes="bananas",
                tone=Tone(tone="sad"),
            ),
            Descriptors(
                likes="cartoons",
                tone=Tone(tone="funny"),
            ),
        ]
        llm = LLMEngine(id="test_batch_improve")

        prompt = "make this story about a boy named Charlie"
        llm.improve(on="story", to=prompt)

        stories = llm(
            input=descriptors_batch,
            output_type=Story,
        )

        print(type(stories))

        print(stories)

    def test_batch_improve_long_chunks(self):
        class Activity(Type):
            activity: str = Context("the selected activity")

        class Inspiration(Type):
            choices: str = Context("potential activities")
            preferences: str = Context("some information about my preferences")

        information = """Boy, have we got some fun things to do for you! We're talking about an exciting list of things to do to cure your boredom, or give you something to do when you've got nothing going on.

Whether you're sitting alone or with a group of friends, these fun things to do will turn your dull session into an exciting one. You can count on this list to plan your day away!

Scroll through this list to find creative ways to make your hobbies all the more better. With this huge list of things to do, you're bound to find something that shouts out to you, guaranteed!
It's not always easy to come up with things to do on your own. That's why we've put together a list of some of the best things to do that are incredibly fun and will keep you busy and entertained for days!

1. Take A Bartending Class
Ever wondered how your bartender makes those magical cocktails? A bartending class will give you the skills to impress your friends at your next house party.

2. Adopt A Pet Dog
We all need a furry companion to keep us company.

3. Take A Weekend Road Trip
The road trip is a classic American activity. On my list of things to do, it's definitely near the top!

4. Go To A Dance Class.
Dancing relieves stress, is great exercise, and can turn into an awesome social opportunity, too.

5. Give Lots Of (Genuine) Compliments This Week.
Need a little more positivity in your life? Start by putting some out there into the world, and I guarantee some will come back to you.

6. Cook Something New
Don't be discouraged if it doesn't come out right. Try it again on a different day.

7. Attend A Men's Retreat
Taking the time to get away from it all with a like-minded group of guys can be a powerful, even life-changing experience.

8. Go Skinny-Dipping.
A little bit risky, sure... But some of the most interesting and engaging things in life are a bit daring!

9. Try A New Sport
From judo to ping-pong to volleyball, anything that gets you moving is likely to improve your mood and your life.

10. Improve Your Wine Knowledge
Tasting a bunch of wines isn't such a bad way to spend a day -- and you'll end up better prepared to order wine on your next date.

11. Head To The Gym
Kills boredom and benefits both your body and brain.

12. Visit A Museum
A trip down memory lane is a great way to kill boredom.

13. Play Stocks Online
And make money while you're at it.

14. Do A Brewery Tour
See how your favorite brew is made.

15. Outdoor Film Festival
One word - fun!

16. Visit A Flea Market
Grab some great deals at the flea market.

17. Visit Your Parents
This is a great time to catch up with your parents.

18. Make Prank Calls
A prank call is bound to bring some cheer.

19. Visit Your Local Bar And Whine Away Your Problems.
A tot of your favorite drink can brighten an otherwise dull day.

20. Create Your Personal Homepage
Ever had a website? Now's the time to create one.

21. Take A Walk And Enjoy Your Surroundings
Being one with nature is therapeutic.

22. Listen To Music
Your favorite ballads will kill boredom in an instant.

23. Go To Your Local Arcade
Arcade games are the wave.

24. Wash Your Car
Your car could use some TLC.

25. Play Rugby
Great sport to kill time.

26. Fly To Vegas On A Whim
Feeling lucky?

27. Visit Your Local Pool
A swim will wash away the boredom.

28. Watch A Bad Movie
Time to watch that movie you've been avoiding for years.

29. Learn To Play The Guitar.
It will take some time, and that's what you need.

30. Milk A Cow
This should be in your bucket-list.

31. Go Camping
The great outdoors will never fail you.

32. Throw A Party
Invite a few friends over.

33. GO Shopping And Splurge
Have some money to burn?

34. Learn How To Drive A Motorbike
Life on two wheels isn't for the fainthearted.

35. Sing Karaoke
Your vocal chords deserve some attention too.

36. Join An Improv Theater
You'll have a laugh...

37. Film A Cooking Show
This'll work if you've got a bubbly personality and, of course, know how to cook.

38. Make A Scarecrow
It doesn't even have to befall, make one for your yard to scare people away.

39. Host An International Dinner Night
Some of the best food comes from different countries. Just be sure the food comes out good. If not, just order take out! No one will know.

40. Try Your Hand At Painting
Who knows, you might do well and gain new talent.

41. Paint Rocks
Place them as decorations in your garden, or anywhere around your home (if they come out looking nice).

42. Have A Photo Shoot
Get all dolled up and put on your best pose.

43. Have A Costume Night
Nope, it does not need to be halloween.

44. Learn Calligraphy
If you've already got good handwriting, this'll come naturally.

45. Upcycle Your Old Furniture
Your furniture needs a touch up.

46. Write A Manifesto
Get writing...

47. Create An Altered Book
It's an amazing experience.

48. Grow Your Own Bonsai Tree
It will take time and patience.

49. Soap Sculpture
Great if you're artistic.

50. Stone Art
You'll need some skill.

51. Make A Birdhouse/Feeder
This is an great way to kill boredom.

52. Redesign Your Bathroom Or Any Part Of Your House
A fresh start...

53. Start A VLOG Tutorial
This should be on everyone's to-do list.

54. Create An Internet Scavenger Hunt
Sounds like fun, huh?

55. Create A Custom Shadow Box
You need to be handy with your tools.

56. Design Your Own Sweatshirt/T-Shirt
A funny slogan is the icing on the cake.

57. Bake A Cake
Everyone loves cake.

58. Build A Lego Kit
Fun! Fun! Fun!

59. Host A Virtual Murder Mystery
This is actually so much more funner than it sounds.

60. Keep In Touch With Friends
The internet makes it virtually, super easy to keep in touch with anyone.

61. Write Thank You Emails
If you've got people to thank, emails are the less awkward way to do it.

62. Google Yourself
You'll most likely just find all your old myspace and anime blog accounts.

63. Open An Online Store
Ebay, Amazon, Etsy, or open a store on a website of your own.

64. Explore Life Hacks
Might as well learn some new ways to score at life.

65. Take A Trip Down The YouTube Rabbit Hole
Be careful... Sometimes there's no way out.

66. Take Surveys For Cash
If you didn't know, there's many websites that pay regular people to take surveys. It may not be much money, but it's easy work.

67. FaceTime A Friend Or Family Member
Catch up with all your long distance relationships.

68. Start Blogging
The perfect way to make money about things you're passionate about.

69. Play DOOM
This John Carmack title will keep you glued to your screen for a while.

70. Clean Your Email
Time to clean up your inbox.

71. Join SecondLife.Com
Take a virtual adventure.

72. Listen To Audiobooks
You can find some gems.

73. Take On-Line Quizzes
Kill the boredom with some mind benders.

74. Enroll In An Online Course
Learn something while you're at it.

75. Learn How To Use Python
This is the most popular programming language today.

76. Read Online Comics
Fancy reading comic books?

77. Find The Invisible Cow
LOL!

78. Watch Online Documentaries
This is a rabbit hole you want to get into.

79. Sell Stuff Online
get rid of the stuff you no longer need.

80. Do A Puzzle
Challenge yourself with the biggest puzzle you can find in your home.

81. Teach Your Pet New Tricks
You and your pet will both benefit from this.

82. Create A Home Office
Home offices are the best place to get any work done that you have. School work, tax filing, even coloring...

83. Explore A New Recipe
Don't worry if you get it wrong the first time. That's usually what happens.

84. Volunteer To Babysit For A Friend
This can be a fun experience if you enjoy kids. Put together some fun activities and watch the kids face light up.

85. Build A Fort
Bring out all your pillows, blankets, couch cushions, and get building!

86. Scan Your Old Photographs
This should be done whenever you have the time. You'd feel devastated if anything happened to all those precious old pictures.

87. Throw An Indoor Picnic
Who says you need to be outdoors to have a picnic?

88. Meditate
Great for the soul and mind.

89. Do Your Laundry
You have to do it anyway.

90. Fix Broken Stuff Around The House
Time to fix that leak in your sink.

91. Start A Garden
Gardening can be therapeutic.

92. Catch Some Sleep
When is the last time you had a good night's rest?

93. Cook For A Loved One
Sharing a meal with a loved one is a great way to pass time.

94. Update Your Finances
Time to balance your books.

95. Start Doing Your Taxes
It's never too early.

96. Re-Watch Your Favorite Movie
You can't watch it enough times.

97. Organize Your Closet
Do something useful with your time.

98. Watch Funny Cat Videos
These will bring some cheer into your life.

99. Learn A New Language
It can come in handy.

100. Take A Break
Everyone needs a break once in a while.

101. Exercise
Exercise can actually put you in a great mood and, plus, it keeps you looking and feeling healthy.

102. Spend Time With Your Family
Even if you don't like them that much, it's always important to keep up with your family.

103. Find Opportunities To Work From Home
There's tons of them, and since you're already at home, find work, and allow the money to come straight to you.

104. Go To The Library
When's the last time you held an actual book in your hand? And I don't mean ebook.

105. Rearrange The Furniture In Your House
This can really make you feel as if you're living in an entirely different place.

106. Plant A Garden
Grow all sorts of fruits and vegetables to save you money at the market.

107. Volunteer At Your Local Animal Shelter
A selfless act can bring fulfillment.

108. Visit An Art Exhibit
It's therapeutic.

109. Practice Your Photography Skills
You can never be too good.

110. Get To Know Your Neighbors
Say hi.

111. Do A Random Act Of Kindness.
You'll fell much better for it.

112. Visit A Retirement Home And Spend Time With The Elderly
You'll have fun and learn loads.

113. Plant Trees
You have a duty to care for the environment.

114. Declutter Your Home
Get rid of all the clutter.

115. Update Your Resume
You never know when the next job might come calling.

116. Call Your Long Lost Friends
Time to catch up.

117. Re-Stock Your Fridge
Have you run out of your favorite goodies?

118. Spend Time With Your Pets
Your pets need your attention.

119. Soak In The Bath
Absolute bliss.

120. Try To Break A World Record
It doesn't have to be complicated.

via: Unsplash / Robinson Recalde
Spice up your life with these fun and adventurous things to do. Step outside yourself and take risks that are incredibly thrilling. Don't be afraid to try these out. Some of these things may sound completely crazy, but you've got to admit, they're totally worth the fun!

121. Rock Climbing
It doesn't even need to be actual rocks. Go to a rock climbing resort if it's your first time, and you've got no experience.

122. Do Some Mountain Biking
You'll definitely feel the burn and be totally sore in the morning.

123. Bungee Jumping
If you aren't afraid of heights, this is a real thrill.

124. Shark Diving
Don't be afraid. You'll be completely safe inside a cage. I can't say the same for the shark...

125. Attend An Auction
Attend a livestock auction and get yourself a chicken. You'll definitely regret it!

126. Watch Wildlife
Go out in the forest, or simply go to the zoo — it's much safer.

127. Plan Your Next Getaway
And get away from all the stress of your current life.

128 Try A Science Experiment
No need for a science class, there's plenty of youtube videos with DIY science experiments.

via: Unsplash / Marc Rafanell López
Don't go at it alone when there are so many things to do with friends! It really doesn't matter what you're doing, it's always a good time when you've got friends around. But, for the times where you can't seem to figure out what to do, try out one of these fun things to do with friends for a fun time!

129. Volunteer At A Soup Kitchen
You'll leave there feeling great about yourselves knowing that you helped out some less fortunate folks.

130. Play Board Games
The ultimate cure for boardom.

131. Invent Your Own Board Game
Don't you hate all those complicated rules every board game has? Time to invent your own without any rules.

132. Go Fishing
Fishing is always fun, even if all you catch is an old, rubber boot.

133. Play Charades
No need for any equipment. The only game similar to a board game that uses only body parts.

134. Play Card Games
Uno, or any other card game you share with your friends.

135. Host A BBQ Party
Fun and tasty!

136. Play Hide And Seek
This game isn't only for kids. And, since your grown, play hide and seek in the dark for more of a challenge. Or in a park at night, if you're courageous enough.

137. Go Bowling
Bowling is always so much fun with a group of your best buddies.

138. Learn To Juggle
Learn to duo-juggle by tossing the pins to your friends while juggling.

139. Play A Game Of Truth Or Dare
This should be interesting.

140. Plan An Elaborate Prank
Who will be the butt of jokes?

141. Doomsday Prepping
Prepare for the end.

142. Take Out Your High School Yearbook And Reminisce
Journey through time.

143 Bar Hopping
You'll need a bit of energy for this.

144. Shoot Some Hoops
Perfect your layups.

145. Play Billiards
Who's the best shot?

146. Have Your Friends Come Over To Watch A Game.
Have some beers in the fridge.

147. Have A Video Game Party
This should be fun.

148. Play A Pick-Up Game
Sharpen your pick up skills.

6 Fun Things To Do Over Summer
Summer is the time for fun! No school, warm weather, long days, it doesn't get any better than that. And, since the days are so long, you'll need plenty of fun things to do over the summer...

149. Have A Water Balloon Fight
Anything that involves water during the summer is a win.

150. Create A DIY Waterpark At Home
This is not as difficult as it sounds. Get some sprinklers, water slides and kiddie pools to create a water wonderland.

151. Go To The Amusement Park
If your DIY water park fails, make plans to go to an amusement park, and make sure they've got a water park included to keep yourself hydrated.

152. Make Homemade Ice Cream
It's as simple as milk, sugar and ice cubes.

153 Make Bubbles
Dish soap and water are all you need, my friend.

154. Go Swimming
There is no funner activity to do during the summer.

7 Fun Things To Do On A Sunday
Sundays are one of those days you aren't sure if you love or hate — it's a day off, but, it's also a day where you need to get ready for the long week ahead. People don't usually do much on this day, though, there's a lot of fun things to do on a Sunday. And, we've got a few examples!

155. Meal Plan For The Week
Start your week off prepared. You'll thank yourself later.

156. Write In Your Journal
It can actually be very healing to write down your thoughts regularly.

157. Take A Power Nap
The don't call it lazy Sunday for just any reason.

158. Do Yoga
Use Sunday as a starting point for yoga, and move your way up to other days of the week as well.

159. Go On A Bike Ride
If the weather allows it, use this day to catch up on some beneficial activity.

160. Go To The Park
You can bike ride to the park! Two Sunday activities in one!

161. Read
All you need is a great book to keep your mind off Monday morning...

The sun has set and you’re ready to call it a day. But you’re still feeling energized and haven’t a clue what to do with yourself before you hit the sack. We’ve come up with a list of things to do while bored at night to help you make the most of your evening. They’re so good you’ll get excited just going through them.

162. Watch Netflix
Tons of shows to kill the boredom.

163. Rethink Your Entire Life And Think Of New Comebacks To Arguments You Lost.
There's always one of those.

164. Check Your Social Media
Been too busy? Now's the time to check your socials.

165. Reread A Book You Found Interesting.
You'll find it interesting...

166. Watch Back To Back Episodes Of Your Favorite Series
It will keep you at the edge of your seat.

167. Watch The Stars At Night.
Very romantic. Do it with someone special.

168. Write Your WILL
Now is a good time.

169. Fold Different Paper Airplanes And Try Them All Out!
Embrace your inner child.

170. Start A Tongue Twister Night Group.
You'll enjoy this.

171. Eat Something That You Told Yourself You Don't Like.
Everyone deserves a second chance.

9 Fun Things To Do For Your Girlfriend
Need lots of great ideas of fun things to do for your girlfriend? We've got them right here! Impress her by doing things for her that make her adore you. She'll be so grateful to have a guy like you after these things.

172. Make S'mores
If you make them right, your girlfriend might love them s'more than she loves you.

173. Have Hot Chocolate
Now's the time to use that fireplace!

174. Recreate Your Favorite Restaurant Meal
Well, if you're able to. It doesn't hurt to try.

175. Prepare A Bubble Bath
Or a bubbling jacuzzi for two...?

176. Have A Spa Night
Be her very own, personal misuse.

177. Watch The Sunset
On the rooftop of the closest place that gives you a clear view of the sun.

178. Host A Themed Movie Night
And let her choose the theme, and the movie.

179. Write Out Your Bucket List
Nothing's sweeter than planning your last moments together.

180. Make A Homemade Pizza
You'll be surprised at how easy it is.

        """
        descriptors_batch = [
            Inspiration(choices=information, preferences="I like to eat food"),
            Inspiration(choices=information, preferences="I like sports"),
        ]
        llm = LLMEngine(id="test_batch_improve_long")

        activities = llm(
            input=descriptors_batch,
            output_type=Activity,
        )

        print(type(activities))

        print(activities)

        prompt = "suggest wacky activities"
        llm.improve(on="activity", to=prompt)
        activities = llm(
            input=descriptors_batch,
            output_type=Activity,
        )
        print(type(activities))
        print(activities)
