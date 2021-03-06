from twython.api import Twython


class AuthorizedTwitter:
    def __init__(self, consumer_token, consumer_secret, access_token, secret):
        self.t = Twython(consumer_token, consumer_secret, access_token, secret)

    def get_list(self, name):
        lists = self.t.show_owned_lists()
        l = next((l for l in lists['lists'] if l['name'] == name), None)
        if not l:
            l = self.t.create_list(name=name, mode='private')

        return l

    def add_missing_members(self, tw_list, members):
        list_id = tw_list['id']
        current_members = self.t.get_list_members(list_id=list_id)
        current_member_names = set([u['screen_name'].lower() for u in current_members['users']])
        missing_members = members - current_member_names
        self.t.create_list_members(list_id=list_id, screen_name=",".join(missing_members))
        return missing_members


class Twitter:
    def __init__(self, consumer_token, consumer_secret):
        self.t = Twython(consumer_token, consumer_secret)
        self.consumer_token = consumer_token
        self.consumer_secret = consumer_secret

    def generate_access_token(self):
        auth = self.t.get_authentication_tokens()

        print("Please go to {auth_url} for a verification code.".format(**auth))
        verifier = input("Verification code: ")

        twitter = Twython(self.consumer_token, self.consumer_secret, auth['oauth_token'], auth['oauth_token_secret'])
        tokens = twitter.get_authorized_tokens(oauth_verifier=verifier)
        return tokens['oauth_token'], tokens['oauth_token_secret']

    def authenticate(self, access_token, secret):
        return AuthorizedTwitter(self.consumer_token, self.consumer_secret, access_token, secret)
