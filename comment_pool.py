from commet import Comment


class CommentPool(object):

    def __init__(self, all_experts, visible_matrix):
        """A global data structure store current comments.

        Args:
            experts: list of BaseExpert
            visible_matrix: two-dimension numpy array
        """
        self.comments = []
        self.all_experts = all_experts
        self.expert_name_to_id = { expert.name: i for i, expert in enumerate(all_experts) }
        self.visible_matrix = visible_matrix

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def pop_comment(self) -> Comment:
        return self.comments.pop()

    def get_comments(self, expert_name):
        """Get comments by expert's name
        
        Args
            expert_name: str
        """
        id_ = self.expert_name_to_id[expert_name]
        visible_indices = self.visible_matrix[id_]

        comment_list = []
        for comment in self.comments:
            target_id = self.expert_name_to_id[comment.expert.name]
            if visible_indices[target_id] == 1:
                comment_list.append(comment)
        return comment_list
    
    def get_current_comment_text(self):
        comments_text = ''
        if len(self.comments) == 0:
            comments_text = 'There is no comment available, please ignore this section.\n'
        else:
            for comment in self.comments:
                comments_text += comment.expert.name + ': ```' + comment.comment_text + '```\n'
        return comments_text
    
    def __len__(self):
        return len(self.comments)
