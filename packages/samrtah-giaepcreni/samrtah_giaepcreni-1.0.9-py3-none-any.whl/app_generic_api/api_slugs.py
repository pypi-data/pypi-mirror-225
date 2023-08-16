
slugs_list_of_dicts = []

class RegisteredApiSlugs:
    @staticmethod
    def get():
        final_dict = dict()
        for item in slugs_list_of_dicts:
            assert isinstance(item, dict)
            for key in item.keys():
                assert key not in final_dict
            final_dict.update(item)
        return final_dict
