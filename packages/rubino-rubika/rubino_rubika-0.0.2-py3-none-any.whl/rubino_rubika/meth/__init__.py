from requests import post, get
import json
from ..server import servers

class meth:
	def __init__(self, auth, profile_id):
		self.auth = auth
		self.profile_id = profile_id
	get_profile_info = lambda self, profile_id: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "target_profile_id": profile_id
  },
  "method": "getProfileInfo"
}).json()
	follow = lambda self, profile_id_t: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "followee_id": profile_id_t,
    "f_type": "Follow",
    "profile_id": self.profile_id
  },
  "method": "requestFollow"
}).json()
	unfollow = lambda self, profile_id_t: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "followee_id": profile_id_t,
    "f_type": "Unfollow",
    "profile_id": self.profile_id
  },
  "method": "requestFollow"
}).json()
	like_post = lambda self, post_profile_id, post_id: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "post_id": post_id,
    "post_profile_id": post_profile_id,
    "action_type": "Like"
  },
  "method": "likePostAction"
}).json()
	unlike_post = lambda self, post_profile_id, post_id: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "post_id": post_id,
    "post_profile_id": post_profile_id,
    "action_type": "Unlike"
  },
  "method": "likePostAction"
}).json()
	post_bookmark = lambda self, post_profile_id, post_id: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "post_id": post_id,
    "post_profile_id": post_profile_id,
    "action_type": "Bookmark"
  },
  "method": "postBookmarkAction"
}).json()
	post_unbookmark = lambda self, post_profile_id, post_id: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "post_id": post_id,
    "post_profile_id": post_profile_id,
    "action_type": "Unbookmark"
  },
  "method": "postBookmarkAction"
}).json()
	get_setting = lambda self: json.loads(json.dumps(post(servers.server4(1), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {},
  "method": "getSettings"
}).json()))
	get_new_event = lambda self: post(servers.server6(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "profile_id": self.profile_id,
    "limit": 20,
    "sort": "FromMax",
    "max_id": "16804580798005623299833"
  },
  "method": "getNewEvents"
}).json()
	get_my_profile_info = lambda self: post(servers.server18(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "profile_id": self.profile_id
  },
  "method": "getMyProfileInfo"
}).json()
	get_explore_posts = lambda self: post(servers.server4(2), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "profile_id": self.profile_id,
    "limit": 21,
    "sort": "FromMax",
    "max_id": "v6-ai-64d89b5b9dc6d662a903a1b463a621023b7750532949295263bc02f49dc6d643efa378a864d8c1e83b775027f32708a4!2"
  },
  "method": "getExplorePosts"
}).json()
	get_shop = lambda self: post(servers.servershop(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "tag_id": "tag*pushak",
    "view_version": "1",
    "limit": 10
  },
  "method": "getTagObjects"
}).json()
	get_suggested = lambda self: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "profile_id": self.profile_id,
    "limit": 20,
    "sort": "FromMax"
  },
  "method": "getSuggested"
}).json()
	search_username = lambda self, search: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "username": search,
    "limit": 20,
    "profile_id": self.profile_id
  },
  "method": "searchProfile"
}).json()
	add_comment = lambda self, post_id, post_profile_id, text: post(servers.server14(), json={
  "auth": self.auth,
  "api_version": "0",
  "client": {
    "app_name": "Main",
    "app_version": "2.0.6",
    "package": "m.rubika.ir",
    "platform": "PWA"
  },
  "data": {
    "content": text,
    "post_id": post_id,
    "post_profile_id": post_profile_id,
    "profile_id": self.profile_id
  },
  "method": "addComment"
}).json()
	username_info = lambda self, username: post(servers.server14(),json={
  "api_version": "0",
  "auth": self.auth,
  "client": {
    "app_name": "Main",
    "app_version": "2.2.1",
    "package": "ir.resaneh1.iptv",
    "platform": "Android"
  },
  "data": {
    "username": username
  },
  "method": "isExistUsername"
}).json()

