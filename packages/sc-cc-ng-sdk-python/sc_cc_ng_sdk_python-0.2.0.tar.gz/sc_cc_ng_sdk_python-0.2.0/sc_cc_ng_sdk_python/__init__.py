import asyncio
import aiohttp

from dataclasses import dataclass, field
from requests import post
from sc_cc_ng_models_python import ContextFilter, BitVal
from typing import List, Optional, Any
from enum import Enum
from itertools import chain
from more_itertools import batched
from functools import reduce

@dataclass
class Result:

    """
        A result object, containing data if everything was ok else an error.
    """

    data:   Optional[Any]   = None
    error:  Optional[str]   = None


@dataclass
class SCNG:

    url: str

    @staticmethod
    def _bit_list_json_query(tokens_list: List[List[str]], context_filter: Optional[ContextFilter] = None) -> dict:
        if context_filter is None:
            context_filter = ContextFilter.empty()

        return {
            "query": """
                query TokenListListQuery(
                    $tokenList: [[String!]!]!,
                    $contextFilter: ContextFilter,
                ) {
                    tokenListBasedContent(
                        tokenList: $tokenList
                        contextFilter: $contextFilter
                    ) {
                        context
                        value
                        reason
                    }
                }
            """,
            "variables": {
                "tokenList": tokens_list,
                "contextFilter": context_filter.to_dict(),
            }
        }

    @staticmethod
    def _dict_list_json_query(tokens_list: List[List[str]], context_filter: Optional[ContextFilter] = None) -> dict:
        if context_filter is None:
            context_filter = ContextFilter.empty()
        return {
            "query": """
                query TokenListDictQuery(
                    $tokenList: [[String!]!]!,
                    $contextFilter: ContextFilter,
                ) {
                    tokensListBasedContentAsDict(
                        tokenList: $tokenList
                        contextFilter: $contextFilter
                    )
                }
            """,
            "variables": {
                "tokenList": tokens_list,
                "contextFilter": context_filter.to_dict(),
            }
        }

    @staticmethod
    def _bit_list_to_string_list(bit_lists: List[List[dict]], ignore_context: bool = False) -> List[List[str]]:

        """
            Converts a list of lists of BitVals to a list of lists of strings.
        """

        return list(
            map(
                lambda xs: list(
                    map(
                        lambda x: x.to_string(
                            simple=ignore_context,
                        ),
                        xs
                    )
                ),
                bit_lists
            )
        )

    def to_dict_list(
        self, 
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> Result:

        """
            Converts lists of tokens to a list of dictionaries, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the dictionary will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """
        try:
            response = post(
                self.url,
                json=self._dict_list_json_query(
                    tokens_list,
                    context_filter,
                ),
            )
            if response.status_code == 200:
                json = response.json()
                if "errors" in json:
                    return Result(error=json["errors"])
                else:
                    return Result(data=response.json()['data']['tokensListBasedContentAsDict'])
            else:
                return Result(error=response.text)
        except Exception as e:
            return Result(error=str(e))
    
    def to_bit_list(
        self,
        tokens_list: List[List[str]],
        context_filter: Optional[ContextFilter] = None,
    ) -> Result:

        """
            Converts lists of tokens to a list of bit values, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """

        try:
            response = post(
                self.url,
                json=self._bit_list_json_query(
                    tokens_list, 
                    context_filter,
                )
            )
            if response.status_code == 200:
                json = response.json()
                if "errors" in json:
                    return Result(error=json["errors"])
                else:
                    return Result(
                        data=list(
                            map(
                                lambda xs: list(
                                    map(
                                        lambda x: BitVal(
                                            context=x['context'],
                                            value=x['value'],
                                            reason=x['reason'],
                                        ),
                                        xs
                                    )
                                ),
                                response.json()['data']['tokenListBasedContent']
                            )
                        )
                    )
            else:
                return Result(error=response.text)
        except Exception as e:
            return Result(error=str(e))

    def to_string_list(
        self, 
        tokens_list: list,
        context_filter: Optional[ContextFilter] = None,
        ignore_context: bool = False,
    ) -> Result:
            
        """
            Converts lists of tokens to a list of strings, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.

            :return: A result object.
        """

        try:
            internal_result = self.to_bit_list(
                tokens_list=tokens_list,
                context_filter=context_filter,
            )
            if internal_result.error is None:
                return Result(
                    data=self._bit_list_to_string_list(
                        internal_result.data,
                        ignore_context=ignore_context,
                    )
                )
            else:
                return internal_result
        except Exception as e:
            return Result(error=str(e))


@dataclass
class ResultAsync:

    """
        A result object, containing data if everything was ok else an error.
    """

    data:   List[Optional[str]]   = field(default_factory=lambda: [])
    error:  List[Optional[str]]   = field(default_factory=lambda: [])

@dataclass
class SCNGAsync:

    url: str

    @staticmethod
    def _compile_batched_result(results: List[Result]) -> ResultAsync:

        """"""

        return ResultAsync(
            data=list(
                chain(
                    *map(
                        lambda x: x.data, 
                        results
                    )
                )
            ),
            error=list(
                filter(
                    lambda x: x is not None,
                    map(
                        lambda x: x.error, 
                        results
                    )
                )
            ),
        )

    async def _fetch_batch(self, session, data, query_fn, response_keys: list, context_filter: Optional[ContextFilter] = None) -> ResultAsync:

        """
            Fetch single batch of data from the server.
        """

        try:
            async with session.post(
                self.url, 
                json=query_fn(
                    data, 
                    context_filter,
                )
            ) as response:
                result = await response.json()
                return Result(
                    data=reduce(
                        lambda x,y: x.get(y), 
                        response_keys, 
                        result
                    )
                )
        except Exception as e:
            return Result(error=str(e))

    async def to_dict_list(self, tokens_list, context_filter: Optional[ContextFilter] = None, batch_size: int = 5, seq_size: int = 4) -> ResultAsync:

        """
            Converts lists of tokens to a list of dicts, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.
            :param batching: The batching mode. Can be 'auto', 'none' or 'manual'.

            :return: A result object.
        """
        try:
            final = []
            async with aiohttp.ClientSession() as session:
                for super_batch in map(
                    lambda super_batch: map(
                        lambda batch: asyncio.ensure_future(
                            self._fetch_batch(
                                session,
                                batch,
                                SCNG._dict_list_json_query,
                                [
                                    'data',
                                    'tokensListBasedContentAsDict',
                                ],
                                context_filter,
                            )
                        ),
                        super_batch,
                    ),
                    batched(
                        batched(
                            tokens_list,
                            batch_size,
                        ),
                        seq_size,
                    )
                ):
                    final.append(
                        await asyncio.gather(*super_batch)
                    )

            result = self._compile_batched_result(
                list(
                    map(
                        self._compile_batched_result,
                        final
                    )
                )
            )

            return ResultAsync(
                data=result.data,
                error=list(
                    chain(*result.error),
                )
            )
        except Exception as e:
            return Result(error=str(e))
    
    async def to_bit_list(self, tokens_list, context_filter: Optional[ContextFilter] = None, batch_size: int = 10, seq_size: int = 4) -> ResultAsync:

        """
            Converts lists of tokens to a list of bits, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.
            :param batching: The batching mode. Can be 'auto', 'none' or 'manual'.

            :return: A result object.
        """
        try:
            final = []
            async with aiohttp.ClientSession() as session:
                for super_batch in map(
                    lambda super_batch: map(
                        lambda batch: asyncio.ensure_future(
                            self._fetch_batch(
                                session,
                                batch,
                                SCNG._bit_list_json_query,
                                [
                                    'data',
                                    'tokenListBasedContent',
                                ],
                                context_filter,
                            )
                        ),
                        super_batch,
                    ),
                    batched(
                        batched(
                            tokens_list,
                            batch_size,
                        ),
                        seq_size,
                    )
                ):
                    final.append(
                        await asyncio.gather(*super_batch)
                    )

            result = self._compile_batched_result(
                list(
                    map(
                        self._compile_batched_result,
                        final
                    )
                )
            )

            return ResultAsync(
                data=list(
                    map(
                        lambda xs: list(
                            map(
                                lambda x: BitVal(
                                    context=x['context'],
                                    value=x['value'],
                                    reason=x['reason'],
                                ),
                                xs
                            )
                        ),
                        result.data,
                    )
                ),
                error=list(
                    chain(*result.error),
                )
            )

        except Exception as e:
            return Result(error=str(e))

    async def to_string_list(self, tokens_list, context_filter: Optional[ContextFilter] = None, batch_size: int = 10, seq_size: int = 4, ignore_context: bool = False) -> ResultAsync:

        """
            Converts lists of tokens to a list of strings, containing
            all matching meta data to those tokens. If no meta data was found
            for a combination of tokens, the list will be empty.

            :param tokens_list: A list of lists of tokens.
            :param context_filter: A context filter object.
            :param batching: The batching mode. Can be 'auto', 'none' or 'manual'.

            :return: A result object.
        """
        try:
            final = []
            async with aiohttp.ClientSession() as session:
                for super_batch in map(
                    lambda super_batch: map(
                        lambda batch: asyncio.ensure_future(
                            self._fetch_batch(
                                session,
                                batch,
                                SCNG._bit_list_json_query,
                                [
                                    'data',
                                    'tokenListBasedContent',
                                ],
                                context_filter,
                            )
                        ),
                        super_batch,
                    ),
                    batched(
                        batched(
                            tokens_list,
                            batch_size,
                        ),
                        seq_size,
                    )
                ):
                    final.append(
                        await asyncio.gather(*super_batch)
                    )

            result = self._compile_batched_result(
                list(
                    map(
                        self._compile_batched_result,
                        final
                    )
                )
            )

            return ResultAsync(
                data=SCNG._bit_list_to_string_list(
                    map(
                        lambda xs: list(
                            map(
                                lambda x: BitVal(
                                    context=x['context'],
                                    value=x['value'],
                                    reason=x['reason'],
                                ),
                                xs
                            )
                        ),
                        result.data,
                    ),
                    ignore_context=ignore_context,
                ),
                error=list(
                    chain(*result.error),
                )
            )

        except Exception as e:
            return Result(error=str(e))