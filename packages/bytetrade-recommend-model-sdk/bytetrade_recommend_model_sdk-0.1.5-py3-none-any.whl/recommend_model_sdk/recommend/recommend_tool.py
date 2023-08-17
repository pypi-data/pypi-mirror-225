import faiss
import numpy as np
from datetime import datetime


from recommend_model_sdk.tools.common_tool import CommonTool
from recommend_model_sdk.mind_sdk.config.content_similar_config import ContentSimilarConfig
from recommend_model_sdk.mind_sdk.model.content_similar_model import ContentSimilarModelRecall
from recommend_model_sdk.mind_sdk.model.content_similar_model import WeaviateContentSimilarModelRecall
from recommend_model_sdk.recommend.common_enum import VectorStoreEnum

class RecommendTool:

    def __init__(self, base_document_id_to_embedding,
                 pretrained_item_embedding_model_name,
                 pretrained_item_embedding_model_version,vector_store = VectorStoreEnum.FAISS) -> None:
        """_summary_
        if vector_store is WEAVIATE:
            WEAVIATE IS NOT NECESSARY, can pass a empty dict {}
        else:
            pass
        

        Args:
            base_document_id_to_embedding (_type_): _description_
            {
                "document_id":{
                    "embedding":[],numpy
                    "created_at": datetime
                }
            }

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """
        if isinstance(vector_store,VectorStoreEnum) is False:
            raise ValueError("vector_store is not VectorStoreEnum")
        self.__vector_store = vector_store
        content_config = ContentSimilarConfig(pretrained_item_embedding_model_name,pretrained_item_embedding_model_version)
        if self.__vector_store == VectorStoreEnum.FAISS:
            self.__faiss_content_similar_model = ContentSimilarModelRecall(base_document_id_to_embedding,content_config)
        elif self.__vector_store == VectorStoreEnum.WEAVIATE:
            self.__weaviate_content_similar_model = WeaviateContentSimilarModelRecall(content_config)
        self.__common_tool = CommonTool()
        self.__logger = self.__common_tool.get_logger()

    
    def __recall_content_similar(self,candidate_document_id_to_document_info,limit = 100,
                                 package_range_list=None,start_time=None,end_time=None,
                                 major_language=None,category_list=None):
        if self.__vector_store == VectorStoreEnum.FAISS:
            url_weight_tuple_list = self.__faiss_content_similar_model.recall(candidate_document_id_to_document_info,limit)
        elif self.__vector_store == VectorStoreEnum.WEAVIATE:
            url_weight_tuple_list = self.__weaviate_content_similar_model.recall(candidate_document_id_to_document_info,limit,package_range_list,start_time,end_time,major_language,category_list)
            
        return url_weight_tuple_list
    
    def __rank_content_similar(self):
        pass
    
    def recommend(self,candidate_document_id_to_document_info,rank_limit=100,
                  start_time=None,end_time=None,
                  major_language=None,category_list=None):
        """_summary_

        Args:
            candidate_document_id_to_document_info (_type_): _description_
            rank_limit (int, optional): _description_. Defaults to 100.
            package_range_list (_type_, optional): _description_. Defaults to None. [str,str]
            start_time (_type_, optional): _description_. Defaults to None. datetime
            end_time (_type_, optional): _description_. Defaults to None. dateime 
            major_language (_type_, optional): _description_. Defaults to None. 
            category_list (_type_, optional): _description_. Defaults to None. [str,str,str]

        Returns:
            _type_: _description_
        """
        if self.__vector_store == VectorStoreEnum.WEAVIATE:
            if major_language is None:
                raise ValueError("when vector store is weaviate, major_language is must")
        self.__logger.debug(f'major_language {major_language}')
        return self.__recall_content_similar(candidate_document_id_to_document_info,rank_limit,package_range_list=None,
                                             start_time=start_time,end_time=end_time,major_language=major_language,
                                             category_list=category_list)
        
    
