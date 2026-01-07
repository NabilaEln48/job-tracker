class StatusEngine:
    RANKING = {
        "Applied": 1,
        "Interview": 2,
        "Rejected": 3,  
        "Offer": 4
    }

    @staticmethod
    def is_transition_valid(current_status: str, new_status: str) -> bool:
        """
        Only allows moving 'forward' in the funnel.
        """
        # If the new status is 'Offer', it always wins.
        # If current is 'Rejected', we only update if it's 'Interview' or 'Offer'.
        curr_rank = StatusEngine.RANKING.get(current_status, 0)
        new_rank = StatusEngine.RANKING.get(new_status, 0)
        
        return new_rank > curr_rank