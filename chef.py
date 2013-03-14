def d(m, s):
    raw_input(m.format(s))

def statement_contains(s, l):
    """Checks to see if s (a list of words) contains an element in l"""
    ####### {v : v \in s AND v \in l} != {}
    return [v for v in s if v in l] != []

class Kitchen:
    """A facility for interpreting the esoteric language 'Chef'."""
    class Error(Exception):
        def __init__(self, title, message):
            self.title = title
            self.message = message
    
    def __init__(self, recipe="", master=None):
        """Constructor
        
        Initializes lists for mixing bowls and baking dishes and
            begins evaluating the recipe (taken in as a string).
        """
        import Bowl
        
        self.food = list()
        with open('food.txt', 'r') as f:
            for line in f:
                self.food.append(line[:-1])
        
        if master is None:
            from collections import deque
            self.ingredients = dict()    # contains a dictionary of ingredients
            self.mixing_bowls = list()    # list of mixing bowls, stack-style
            self.baking_dishes = list() # list of baking dishes, stack-style
            self.stdin = deque()        # Our very own stdin! So we *could* take in more than one character at a time from what the user sees
            self.stdout = deque()        # Well, if we have an stdin, might as well have an stdout. May make life easier.
            self.history = list()        # Contains a list (stack) of (func, arg) tuples, most-recent last. Useful for looping.
        
        #handles a copy constructor
        elif hasattr(master, 'ingredients') and hasattr(master, 'mixing_bowls') and hasattr(master, 'baking_dishes') and hasattr(master, 'stdin') and hasattr(master, 'stdout') and hasattr(master, 'history'):
            self.ingredients = master.ingredients
            self.mixing_bowls = master.mixing_bowls
            self.baking_dishes = master.baking_dishes
            self.stdin = master.stdin
            self.stdout = master.stdout
            
            #self.history        = master.history
            # This statement may interfere with correct looping.
            #
            # Note that how we are storing the history right now allows me to say things like this:
            #
            # >>> self.history.append(self.take, ['pizza', 'from', 'refrigerator'])
            # >>> last_cmd = self.history[-1]
            # (self.take, ['pizza', 'from', 'refrigerator'])
            # >>> last_cmd[0](last_cmd[1])
            # (does that last command again)
            

    def is_food_word (food, foodwords):
        for x in range (len(foodwords)):
            for each in food.split():
                if (foodwords[x]==each):
                    return True
        return False
    
    def has_serves (servingsize):
        for each in servingsize.split():
            if ("Serves" == each):
                return True
        return False
    
    def acceptable_method (method):
        m = []
        failure = [0]
        for x in method:
            for each in x.split('  '):
                if (each.count('.')==1):
                    m.append(each)
                elif(each=='\n'):
                    True
                else:
                    failure.append (each)
                    return failure
        return m
    
    def contains_food_word(x):
        for y in x.split(' '):
            if (is_food_word(y)):
                return True
        return False
            
                    
                
    everything = []
    def ingredients_valid (ingredients):
        i =[0]
        ingre = []
        for x in range (len(ingredients)):
            for each in ingredients[x].split('\n'):
                if (contains_food_word(each)):
                    ingre.append(each)
                else:
                    i.append(each)
                    return i
                break
        return ingre
    
    
    def read_recipe(path):
    	"""Loads the given file and does initial parsing.
    
This method will parse the given filename

See http://docs.python.org/library/doctest.html#module-doctest
So much awesome.

Example output:
>>> print read_recipe("/hw.chef")
["Hello World Souffle", "This recipe prints the immortal words "Hello world!", in a basically brute force way. It also makes a lot of food for one person.", "72 g haricot beans
101 eggs
108 g lard
111 cups oil
32 zucchinis
119 ml water
114 g red salmon
100 g dijon mustard
33 potatoes", "Put potatoes into the mixing bowl. Put dijon mustard into the mixing bowl. Put lard into the mixing bowl. Put red salmon into the mixing bowl. Put oil into the mixing bowl. Put water into the mixing bowl. Put zucchinis into the mixing bowl. Put oil into the mixing bowl. Put lard into the mixing bowl. Put lard into the mixing bowl. Put eggs into the mixing bowl. Put haricot beans into the mixing bowl. Liquefy contents of the mixing bowl. Pour contents of the mixing bowl into the baking dish.

Serves 1."]
        """
        #reads in a file and appends each line to a list called recipe
        F = open (path,'r')
        re = F.readlines()
        recipe = []
        for line in re:
            recipe.append(str(line))
    
        #basic error checks.    If the title does not contain a food word or have a serves statement, the program will not run
        if not is_food_word(recipe[0]):
           return 0
        if not has_serves(recipe[len(recipe)-1]):
            return 1
        else: 
            deletes = 0
            meth = 0
            #checks to see if Ingredients and Method declaration are done correctly
            for p in range (len (recipe)):
                for each in recipe[p].split():
                    if(each == "Ingredients."):
                        if (each.find('.')):
                            #catches missing periods in the method declaration.  Returns 0 if there is no period
                            deletes = p
                        else:
                            deletes = 0
                    if (each == "Method."):
                        if (each.find('.')):
                            #catches missing periods in the method declaration.  Returns 0 if there is no period
                            meth = p+1
                        else:
                            meth = 0
            if (deletes ==0 or meth ==0):
                if (deletes ==0):
                    return 2
                if (meth ==0):
                    return 3
            #if the program passes all of those error checks, then it will create a separate list for ingredients, and a separate list for things to do
            banana= meth
            method = []
            ingredients = []
            #creates a separate list of all the methods to run
            while (meth< len(recipe)):
                method.append(recipe[meth])
                meth = meth+1
            #removes the serves command from the Method list
            serves = method[len(method)-1]
            del method [len(method)-1:len(method)]
            method = acceptable_method (method)
            #handles poor method syntax
            if (method[0] == 0):
                print '\a'
                print "invalid syntax for method.  See line " + "'" + str(method[1]) + "'"
                raise Kitchen.Error("Invalid Syntax","See line {line}.".format(line=method[1]))
                return 4
            #removes the ingredients and method from the list Recipe
            del recipe [banana-1: len(recipe)]
            del recipe[0:deletes+1]
            #recipe  now only contains things we need to deal with. Title and comments are deleted
            for x in recipe:
                ingredients.append(x)
            ingredients = ingredients_valid(ingredients)
            if (ingredients[0]==0):
                print '\a'
                print "invalid syntax for ingredients.    See line " + "'" + str(ingredients[1]) + "'"
                raise Kitchen.Error("Invalid Syntax", "See line {line}.".format(line=ingredients[1]))
                return 5
    
            
            
    def errorhandling ():
        x = read_recipe ('Portalcake.txt')
        if (x ==0):
            print '\a'
            print "Error.  This recipe does not make any food!    Why would I want to eat it?!"
            print "Your recipe is either missing or has an invalid title"
            raise Kitchen.Error("Invalid Syntax", "Your recipe is either missing or has an invalid title.")
        elif (x==1):
            print '\a'
            print "Error! This recipe doesn't serve anyone!     I'm HUNGRY **eats table**"
            raise Kitchen.Error("Invalid Syntax", "This recipe doesn't serve anyone!     I'm HUNGRY **eats table**")
        elif (x==2):
            print '\a'
            print "Invalid Syntax!"
            print "Missing or incorrect     'Ingredients.' tag"
            raise Kitchen.Error("Invalid Syntax", "Missing or incorrect 'Ingredients.' tag")
        elif (x==3):
            print '\a'
            print "Invalid Syntax!"
            print "Missing or incorrect 'Method.' tag"
            raise Kitchen.Error("Invalid Syntax", "Missing or incorrect 'Method.' tag")
        elif (x==4):
            pass
        elif (x==5):
            pass
        
    
    def do(self, s):
        """Does an arbitrary operation from a valid Chef string
        
        The command must be the first word, case sensitive.
        If the command does not exist, None is returned.
        The rest of the string is passed to the desired function as a list.
        
        Author: Sean
        """
        
        def isVerbStatement(li):
            return len(li) == 3 and li[1] == "the" and li[2] in [v + "." for v in self.ingredients]
        
        t = s.split()
        try:
            if s == "Ingredients.":
                self._do_ingredients()
            elif len(t) < 2:
                raise Kitchen.Error("Syntax Error", "Commands must have at least two tokens.")
            elif hasattr(self, t[0]):
                return getattr(self, t[0])(t[1:])
            elif isVerbStatement(t): # the word may be a verb
                print "Verbing!"
                print "Verb:", t[0]
            else:
                print "No such attribute"
            
        except Kitchen.Error as (title, message):
            import sys
            sys.excepthook(*sys.exc_info())
            
            print ""
            print "{t}: {m}\a".format(t=title, m=message)
            return False
    
    def _do_ingredients(self):
    	"""Author: Sean"""
        s = raw_input()
        measures = {"ml":"wet", "l":"wet", "dash":"wet", "dashes":"wet", "g":"dry", "kg":"dry", "pinch":"dry", "pinches":"dry", "cup":None, "cups":None, "teaspoon":None, "teaspoons":None, "tablespoon":None, "tablespoons":None, None:None}
        types = {"heaped":"dry", "level":"dry"}
        while s != "":
            s = self._get_ingredient(s, measures, types)
            self.ingredients[s[0]] = (s[1], s[2])
            s = raw_input()
        
    def __repr__(self):
    	"""Author: Sean"""
        return "  Ingridients: {ing}\n Mixing Bowls: {mb}\nBaking Dishes: {bd}\n Input Buffer: {ip}\nOutput Buffer: {op}".format(ing=str(self.ingredients), mb=str(self.mixing_bowls), bd=str(self.baking_dishes), ip=str(self.stdin), op=str(self.stdout))
    
    # Have this function declare a multidimensional array of strings according to differing degrees of messiness
    # so it can be called
    # ...    return arr[len(mixing_bowls) // 5][len(baking_dishes) // 5]
    # or something like that.
    def __str__(self):
    	"""Author: Sean"""
        return "You see a mess of utensils; you have a lot of work yet to do."
    
    def _get_bowl(self, s):
        """Returns the mixing bowl specified by this string.
        
        This method searches the string provided for the mixing bowl needed:
        >>> getDish("Pour the 3rd mixing bowl into the 2nd baking dish.")
        3
        
        If no ordinal for a mixing bowl is specified, it defaults to 1:
        >>> getDish("Put zucchinis into the mixing bowl.")
        1
        
        If there is no mention of any mixing bowls, this function returns None:
        >>> getDish("I've got poop for brains.")
        None
        
        Author:
        """
        pass
        return 0
    
    def _get_dish(self, s):
        """Returns the baking dish specified by this string.
        
        This method searches the string provided for the baking dish needed:
        >>> getDish("Pour the 3rd mixing bowl into the 2nd baking dish")
        2
        
        If no ordinal for a baking dish is specified, it defaults to 1:
        >>> getDish("Pour the 3rd mixing bowl into the baking dish")
        1
        
        If there is no mention of any baking dishes, this function returns None:
        >>> getDish("I've got poop for brains.")
        None
    	
    	Author:
        """
        pass
        return 0
    
    def _get_ingredient(self, item, measures, types):
        """Takes exactly one string, a dictionary of valid measures, and a dictionary of valid measure-types and returns (name, value, type)
        
        Author: Sean
        """
        name = type = value = explicit_type = None
        s = item.split()
        if len(s) < 1:
            raise Kitchen.Error("Ingredient Error", "Blank line encountered.")
        if s[0].isdigit():
            value = int(s[0])
            if statement_contains(s[1:], measures):
                if s[1] in types:
                    type = types[s[1]]
                    name = s[2:]
                elif s[1] in measures:
                    type = measures[s[1]]
                    name = s[2:]
                else:
                    raise Kitchen.Error("Ingredient Error", "Illegal value or ingredient encountered.")
            else:
                name = s[1:]
        elif s[0] in measures:
            type = measures[s[0]]
            name = s[1:]
            if name == []:
                raise Kitchen.Error("Ingredient Error", "Must specifiy an ingredient name.")    
            elif s[0] in types:
                if s[1] in measures:
                    type = types[type]
                    name = s[2:]
                    if name == []:
                        raise Kitchen.Error("Ingredient Error", "Must specifiy an ingredient name.")
            else:
                raise Kitchen.Error("Ingredient Error", "Must specifiy measure for type.")
        else:
            name = s
        name = ' '.join(name)
        return (name, value, type)
    
    def _get_ingredients(self, l):
        """Takes a list l of ingredient-statements and populates the ingredients.
        
        Author: Sean
        """
        
        if len(l) < 1:
            raise Kitchen.Error("Ingredient Error", "Must have at least one ingredient.")
        
        measures = {"ml":"wet", "l":"wet", "dash":"wet", "dashes":"wet", "g":"dry", "kg":"dry", "pinch":"dry", "pinches":"dry", "cup":None, "cups":None, "teaspoon":None, "teaspoons":None, "tablespoon":None, "tablespoons":None, None:None}
        types = {"heaped":"dry", "level":"dry"}
        
        for item in l:
            ing = self._get_ingredient(item, measures, types)
            self.ingredients[ing[0]] = (ing[1], ing[2])

    
    def Take(self, s):
        """Take (ingredient) from refrigerator.
        
        This reads a numeric value from STDIN into
            the ingredient named, overwriting any
            previous value.
            
        Author: Sean
        """
        
        def isFood(s):
            return not s.isdigit()
        
        ingredient_name = ' '.join(s[:-2])
        
        if not isFood(ingredient_name):
            raise Kitchen.Error("Name Error", "You can't eat {}".format(ingredient_name))
            return False
        elif s[-1] != "refrigerator." or s[-2] != "from":
            raise Kitchen.Error("Syntax Error", "Take <ingredient> from refrigerator.")
            return False
        
        elif len(self.stdin) is 0:
            _in = raw_input("Press enter after input: ")
            if _in.isdigit(): # if the entire input can be parsed as a single number
                self.stdin.append(int(_in)) # append that number to the buffer
                self.ingredients[ingredient_name] = self.stdin.popleft()
            else:
                for char in _in: # otherwise, append the integer value of each character entered to the buffer.
                    self.stdin.append(ord(char))
                self.ingredients[ingredient_name] = self.stdin.popleft()
        
        else:
            self.ingredients[ingredient_name] = self.stdin.popleft()
        
        self.history.append((self.take, s))
        
        return True
    
    def Put(self, s):
        """Put (ingredient) into the [nth] mixing bowl.
        
        This puts the ingredient into the nth mixing bowl.
        """
        pass
        return True
    
    def Fold(self, s):
        """Fold (ingredient) into [nth] mixing bowl.
        
        This removes the top value from the nth mixing bowl and places it in the ingredient.
        """
        pass
        return False
    
    def Add(self, s):
        """Two uses.
        
        
        Add (ingredient) [to [nth] mixing bowl].
            This adds the value of ingredient to the
            value of the ingredient on top of the
            nth mixing bowl and stores the result
            in the nth mixing bowl.
        
        Add dry ingredients [to [nth] mixing bowl].
            This adds the values of all the dry ingredients
            together and places the result into the
            nth mixing bowl.
        """
        pass
        return False
    
    def Remove(self, s):
        """Remove ingredient [from [nth] mixing bowl].
        
        This subtracts the value of ingredient from
            the value of the ingredient on top of the
            nth mixing bowl and stores the result in
            the nth mixing bowl.
        """
        pass
        return False
    
    def Combine(self, s):
        """Combine ingredient [into [nth] mixing bowl].
        
        This multiplies the value of ingredient by
            the value of the ingredient on top of
            the nth mixing bowl and stores the result
            in the nth mixing bowl.
        """
        pass
        return False
    
    def Divide(self, s):
        """Divide ingredient [into [nth] mixing bowl].
        
        This divides the value of ingredient into
            the value of the ingredient on top of
            the nth mixing bowl and stores the result
            in the nth mixing bowl.
        """
        pass
        return False
    
    def Liquefy(self, s):
        """Two uses.
        
        
        Liquefy | Liquify ingredient.
            This turns the ingredient into a liquid,
            i.e. a Unicode character for output purposes.
            
            (Note: The original specification used
            the word "Liquify", which is a spelling
            error. "Liquify" is deprecated.
            Use "Liquefy" in all new code.)
        
        Liquefy | Liquify contents of the [nth] mixing bowl.
            This turns all the ingredients in the nth mixing bowl
            into a liquid, i.e. a Unicode characters for
            output purposes.
        """
        pass
        return False
    
    def Stir(self, s):
        """Two uses.
        
        
        Stir [the [nth] mixing bowl] for number minutes.
            This "rolls" the top number ingredients
            in the nth mixing bowl, such that the
            top ingredient goes down that number of
            ingredients and all ingredients above it
            rise one place. If there are not that many
            ingredients in the bowl, the top ingredient
            goes to tbe bottom of the bowl and all
            the others rise one place.
        
        Stir ingredient into the [nth] mixing bowl.
            This rolls the number of ingredients
            in the nth mixing bowl equal to
            the value of ingredient, such that
            the top ingredient goes down that number
            of ingredients and all ingredients above
            it rise one place. If there are not that
            many ingredients in the bowl, the top
            ingredient goes to tbe bottom of the bowl
            and all the others rise one place.
        """
        pass
        return False
    
    def Mix(self, s):
        """Mix [the [nth] mixing bowl] well.
        
        This randomises the order of the
            ingredients in the nth mixing bowl.
        """
        pass
        return False
    
    def Clean(self, s):
        """Clean [nth] mixing bowl.
        
        This removes all the ingredients
            from the nth mixing bowl.
        
        Author: Sean
        """
        if len(s) > 3 or s[1] != 'mixing' or s[2] != 'bowl.':
            return False
        
        num = self._get_dish(' '.join(s))
        if num == None:
            return False
        
        self.mixing_bowls[num] = list()
        return True
    
    def Pour(self, s):
        """Pour contents of the [nth] mixing bowl into the [pth] baking dish.
        
        This copies all the ingredients from
            the nth mixing bowl to the
            pth baking dish, retaining the order
            and putting them on top of anything
            already in the baking dish.
        """
        pass
        return False
    
    def Set(self, s):
        """Set aside.
        
        This causes execution of the innermost
            loop in which it occurs to end
            immediately and execution
            to continue at the statement after
            the "until".
        """
        pass
        return False
    
    def Serve(self, s):
        """Two uses.
        
        
        Serve with auxiliary-recipe.
            This invokes a sous-chef to immediately
            prepare the named auxiliary-recipe.
            The calling chef waits until the sous-chef
            is finished before continuing.
            
            See the section on auxiliary recipes below.
        
        Serves number-of-diners.
            This statement writes to STDOUT the contents
            of the first number-of-diners baking dishes.
            It begins with the 1st baking dish,
            removing values from the top one by one and
            printing them until the dish is empty,
            then progresses to the next dish, until all
            the dishes have been printed.
            
            The serves statement is optional, but is
            required if the recipe is to output anything!
        """
        for dish in self.baking_dishes:
        	pass
        return False
    
    def Refrigerate(self, s):
        """Refrigerate [for number hours].
        
        This causes execution of the recipe
            in which it appears to end immediately.
            If in an auxiliary recipe, the auxiliary
            recipe ends and the sous-chef's first
            mixing bowl is passed back to the calling
            chef as normal. If a number of hours is
            specified, the recipe will print out its
            first number baking dishes before ending.
        """
        pass
        return False
    
    def _verb_(self, s):
        """Takes care of VERB until VERBED.
        Not a clue on how to do this yet.
        
        IDEA!
         -- Create a new kitchen
         -- keep reading in commands until verbed
         -- pass commands to a new kitchen
         -- once we reach 'until verbed', execute the history again
         -- keep executing until condition is zero
        """

        pass

def read_recipe(filepath):
    """Loads the given *.chef file and does initial parsing.
    
This method will parse the given filename

See http://docs.python.org/library/doctest.html#module-doctest
So much awesome.

Example output:
>>> print read_recipe("/hw.chef")
["Hello World Souffle", "This recipe prints the immortal words "Hello world!", in a basically brute force way. It also makes a lot of food for one person.", "72 g haricot beans
101 eggs
108 g lard
111 cups oil
32 zucchinis
119 ml water
114 g red salmon
100 g dijon mustard
33 potatoes", "Put potatoes into the mixing bowl. Put dijon mustard into the mixing bowl. Put lard into the mixing bowl. Put red salmon into the mixing bowl. Put oil into the mixing bowl. Put water into the mixing bowl. Put zucchinis into the mixing bowl. Put oil into the mixing bowl. Put lard into the mixing bowl. Put lard into the mixing bowl. Put eggs into the mixing bowl. Put haricot beans into the mixing bowl. Liquefy contents of the mixing bowl. Pour contents of the mixing bowl into the baking dish.

Serves 1."]
    """
    pass

# takes the instruction string from earlier and splits it into statements
def preheat(method):
    """Takes all of the statements (as a single string) under Method and begins the parsing process.
    
This method returns a list of simple tuples where the first element is the command
and the second element is the source string. The output of this method is intended
for calling Mom.
    """
    pass

def gather(ingredients):
    """Return a dictionary of ingredients from the given string.
    
The dictionary returned will contain the ingredient as a string
mapped to a tuple, where the first element indicates if it is dry or wet
and the second element denotes its numeric value.

Example:
    {'apple':('dry', 96), 'oil':('wet', 59), etc.}
    """
    pass

# Because we all know her handwriting is horrid.
# we may be able to make this fun by using advanced features of functions in Python
def callMom(method):
    """Takes a list of command-string tuples and returns a list of pure command-tuples.
    
Following is a list of commands and descriptions, following the pattern
(<command>,     <arguments>)    - execute <command> with <arguments>
where the default value of ## is exactly 1 (signifying the mixing bowl index
and where # is a plain number

For overloaded commands, use hasattr() for type checking

('take',     'ingredient')                   - get one character from the user and place its numeric value into ingredient
('put',         'ingredient', ##)               - push the ingredient onto the ##th mixing bowl
('fold',     'ingredient', ##)               - pop the ##th mixing bowl into the ingredient
('add',         'ingredient', ##)               - peek at the ##th mixing bowl and add (numerically) ingredient to it
('remove',     'ingredient', ##)               - peek at the ##th mixing bowl and subtract (numerically) ingredient from it
('combine',     'ingredient', ##)               - peek at the ##th mixing bowl and multiply (numerically) ingredient with it
('divide',     'ingredient', ##)               - peek at the ##th mixing bowl and divide (numerically) ingredient from it
('add', ##)                                   - takes all of the dry ingredients and places the sum into the #th mixing bowl
('liquefy',     'ingredient')                   - transform the ingredient into its Unicode equivalent
('liquefy',      ##)                           - transform the contents of the ##th mixing bowl into their Unicode equivalents
('stir',      ##,            #)               -
('stir',     'ingredient',    ##)               -
('mix',           ##)                           - randomize the order of the ##th mixing bowl
('clean',       ##)                           - pop the ##th mixing bowl until empty
('loop',      'verb',       'ingredient')   - See after.
('next',      'verb',       'ingredient')   - See after.
('exit')                                   - Continues execution after the next 'next'
('serve',      'recipe')                       - Invokes the execution of another recipe
('fridge')                                   - Ends execution immediately and returns the first mixing bowl
('fridge, #)                               - Print out the first # baking dishes before calling ('fridge')

('serves', #)                               - Pops and prints each baking dish in succession. This is the last command.

Note that everything that follows the 'serve' command is an auxiliary recipe.

Looping:
   With the 'loop' command, if the ingredient is non-zero, continue execution until reaching the 'next' command. If the ingredient is zero, continue execution after a matching 'next'.
   At the 'next' command, if an ingredient is given (defaulting to the ingredient given by 'loop'), continue execution at the previous 'loop' if the given ingredient is non-zero. If the ingredient is zero, simply continue.

The output of this method is intended for cooking.
    """
    
    pass

def loadVerbs(path):
    """Return a list verbs and their past-tense form read from a file with the given path.
        
The return will be a list of tuples containing two strings:
the first being the infinite stem, the second being the simple past.

Example:
    [("sift","sifted"),("boil","boiled"), ...]
    """
    pass

def loadFoods(path):
    """ Returns a simple list of foods read from a file with the given path."""
    pass

# executes a list of commands
def cook(ingredients, method):
    """Execute the list of commands given using the ingredients provided.
    
Execute the given list of commands in the format given by calling Mom.
It is an error if a given command does not exist.
    """
    
    ###################################################
    
    # iterate through the commands with complete control over position
    #    (python's for-each loop does not give you any control)
    cmd_index = 0
    while cmd_index < len(method):
        cmd_index += 1
        pass
    
    pass


########################################


print statement_contains("hello world".split(), ["hello", "poop"])

hat = 'c= '

kills = ["quit", "exit", "stop", "kill", "term"]

k = Kitchen()

cmd = raw_input(hat)
while cmd[:4] not in kills: # checks the first four letters
    k.do(cmd)
    print repr(k)
    cmd = raw_input(hat)