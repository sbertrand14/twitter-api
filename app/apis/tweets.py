from flask_restplus import Namespace, Resource, fields
from flask import abort
from app.models import Tweet
from app import db

api = Namespace('tweets')

json_tweet = api.model('Tweet', {
    'id': fields.Integer,
    'text': fields.String,
    'created_at': fields.DateTime
})

json_new_tweet = api.model('New tweet', {
    'text': fields.String(required=True)
})

json_list_tweet = api.model('TweetList', {
    'tweets': fields.List(fields.Nested(json_tweet))
})


@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
@api.param('id', 'The tweet unique identifier')
class TweetResource(Resource):
    @api.marshal_with(json_tweet)
    def get(self, id):
        tweet = Tweet.query.get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            return tweet

    @api.marshal_with(json_tweet, code=200)
    @api.expect(json_new_tweet, validate=True)
    def patch(self, id):
        tweet = Tweet.query.get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            tweet.text = api.payload["text"]
            db.session.commit()
            return tweet

    def delete(self, id):
        tweet = Tweet.query.get(id)
        if tweet is None:
            api.abort(404, "Tweet {} doesn't exist".format(id))
        else:
            db.session.delete(tweet)
            db.session.commit()
            return None

@api.route('')
class TweetsResource(Resource):
    @api.marshal_with(json_list_tweet, code=200)
    def get(self):
        tweets = db.session.query(Tweet).all()
        return tweets

    @api.response(422, 'Invalid tweet')
    @api.marshal_with(json_tweet, code=201)
    @api.expect(json_new_tweet, validate=True)
    def post(self):
        text = api.payload["text"]
        if len(text) > 0:
            tweet = Tweet()
            tweet.text = text
            db.session.add(tweet)
            db.session.commit()
            return tweet, 201
        else:
            return abort(422, "Tweet text can't be empty")
