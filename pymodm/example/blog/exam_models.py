from pymodm import MongoModel, EmbeddedMongoModel, fields, connect


# Establish a connection to the database.
connect('mongodb://localhost:27017/blog')


class Merchant(MongoModel):
    # We set "blank=False" so that values like the empty string (i.e. u'')
    # aren't considered valid. We want a real title.  As above, we also make
    # most fields required here.
    name = fields.CharField(required=True, blank=False)
    description = fields.CharField(required=True)
    # Comments will be stored as a list of embedded documents, rather than
    # documents in their own collection. We also set "default=[]" so that we can
    # always do:
    #
    #     post.comments.append(Comment(...))
    #
    # instead of:
    #
    #     if post.comments:
    #         post.comments.append(Comment(...))
    #     else:
    #         post.comments = [Comment(...)]
