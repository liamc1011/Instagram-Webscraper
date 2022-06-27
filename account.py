class Account:
    __slots__ = ['username', 'name', 'follows_you', 'you_follow']

    def __init__(self, username, name, follows_you=False, you_follow=False):
        self.username = username
        self.name = name
        self.follows_you = follows_you
        self.you_follow = you_follow

    def bool_to_words(self, boolean):
        if boolean == True:
            return 'yes'
        else:
            return 'no'

    def __str__(self):
        return f"{self.username} ({self.name}) || follower: {self.bool_to_words(self.follows_you)} following: {self.bool_to_words(self.you_follow)}"

def main():
    hp = Account('piggy', 'Piggold III', you_follow=True)
    print(hp)

if __name__ == '__main__':
    main()