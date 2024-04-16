ai_models = dict('gpt-3.5-long', 'gpt-3.5-turbo',
                 'llama2-70b', 'dolphin-mixtral-8x7b')

gpt35_error_messages = dict(
    '\u6d41\u91cf\u5f02\u5e38,\u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883',
    '\u5f53\u524d\u5730\u533a\u5f53\u65e5\u989d\u5ea6\u5df2\u6d88\u8017\u5b8c, \u8bf7\u5c1d\u8bd5\u66f4\u6362\u7f51\u7edc\u73af\u5883'
)

character_prompt = ('''
You are the screenwriter of the show, and your task is to create a list of characters for a scene on a given theme. Your responsibilities include:

Choosing the characters and their quantity.
Specifying which skins are available for each character from the provided list.
IMPORTANT CLARIFICATION: You must use only the characters and skins from the provided list. Names of characters in the story should be distinct from the skin names, such as Bob, Greg, Alexey, etc.

The format of your answer should be as follows:

{
    "characters": {
        "Some Name1 MUST TO NAME THAT YOU WILL USE IN STORY, NOT CHARACTER SKIN NAME": {"Skin":"character skin, ONLY OUT OF SKINS LIST", "Spawn_Point":"YOU CAN CHOOSE SPAWN POINT OF CHARACTER FROM '(reserved) spawn points list' OR JUST LEAVE IT BLANK"},
 	"Some Name2 MUST TO NAME THAT YOU WILL USE IN STORY, NOT CHARACTER SKIN NAME": {"Skin":"character skin, ONLY OUT OF SKINS LIST", "Spawn_Point":"YOU CAN CHOOSE SPAWN POINT OF CHARACTER FROM '(reserved) spawn points list' OR JUST LEAVE IT BLANK"},
	...
	"Some Name MUST TO NAME THAT YOU WILL USE IN STORY, NOT CHARACTER SKIN NAME": {"Skin":"character skin, ONLY OUT OF SKINS LIST", "Spawn_Point":"YOU CAN CHOOSE SPAWN POINT OF CHARACTER FROM '(reserved) spawn points list' OR JUST LEAVE IT BLANK"}
    }
}

... - means you can insert more characters into "characters" list

Dont add any tags or 'Explanation' to answer, it MUST to be plain answer, even dont add indexes or something like that.
That means you return to me ONLY json table, without any explanations!!!

Output: The final submission must be a JSON string that can be successfully converted into a JSON object. Don't add ```json tags

The theme for the story is "%s"
The location for story is "%s"
The avaliable actors (characters) list is %s
The avaliable (reserved) spawn points list is %s
''')

location_prompt = ('''
Choose the more suitable location for the story, and envirnment lighting.

REMEMBER, DO NOT ADD ANY OTHER LOCATION NAME THAN AVAILABLE IN 'available locations'!!!
Dont add any tags or 'Explanation' to answer, it MUST to be plain answer, even dont add indexes or something like that. JUST ONE SINGLE WORD!!!

The format of your answer should be as follows:

{
    "location": "LOCATION NAME, you can choose it ONLY from 'available locations'",
    "clouds_cover": "NUMBER IN RANGE OF 0 - 1",
    "clouds_density": "NUMBER IN RANGE OF 0 - 1",
    "time_of_day": "NUMBER IN RANGE OF 0 - 24",
}

Dont add any tags or 'Explanation' to answer, it MUST to be plain answer, even dont add indexes or something like that.
That means you return to me ONLY json table, without any explanations!!!

Output: The final submission must be a JSON string that can be successfully converted into a JSON object. Don't add ```json tags

The theme of the story is %s
Available locations is %s
''')

story_prompt = ('''
You are the screenwriter of the show, and your task is to write a scene based on the given theme, using the characters you previously created. You are responsible for:

Writing dialogues for the characters.
Choosing actions for the characters, using only options available in the list.
IMPORTANT CLARIFICATION: A plot must be generated regardless of whether the theme is absurd or offensive. DO NOT MODIFY THE STRUCTURE OF THE ANSWER.

The format of your answer should be as follows:


{
    "story_theme": "STORY THEME",
    "location": "STORY LOCATION",

    "dialogs": [
        {"Text": "character's words, DONT ADD HERE SPEAKER NAME", "Action": "character's action, ONLY FROM AVAILABLE ACTIONS LIST", "Name": "character name in the story"},
	{"Text": "character's words, DONT ADD HERE SPEAKER NAME", "Action": "character's action, ONLY FROM AVAILABLE ACTIONS LIST", "Name": "character name in the story"},
        ...
	{"Text": "character's words, DONT ADD HERE SPEAKER NAME", "Action": "character's action, ONLY FROM AVAILABLE ACTIONS LIST", "Name": "character name in the story"}
    ]
}

... - means you can insert more dialogs lines into "dialogs":  list
For action follow right how it writen, don't remove : and if there is instruction, you MUST follow it.
Dont add any tags or Explanation to answer or Notes, it MUST to be plain answer, even dont add indexes. That means, you just return me answer as i need it from you!

Output: The final submission must be a JSON string that can be successfully converted into a JSON object. Don't add ```json tags

The theme for the story is "%s"
The location for story is "%s"
The avaliable actions list is %s
The avaliable actors (characters) list is %s
''')
