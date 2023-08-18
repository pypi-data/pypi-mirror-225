import re
import pandas as pd
from typing import (
    List,
    Dict,
    Optional
)
from dataclasses import dataclass
from mjjo import Log
from mjjo.bjd import Bjd


@dataclass
class ConvAddr():


    def __init__(self):
        self.bjd_current_dic: Dict[str, str] = None
        self.bjd_smallest_list: List[str] = None
        self.bjd_current_bjd_nm_list: List[str] = None
        self.multiple_word_sgg_list: List[str] = None
        self.current_sido_sgg_list: List[str] = None
        self.current_sido_list: List[str] = None
        self.current_sgg_list: List[str] = None
        self.current_emd_list: List[str] = None
        self.current_ri_list: List[str] = None
        self.bjd_changed_dic: Dict[str, str] = None
        self.bjd_changed_old_bjd_nm_list: List[str] = None
        self.logger = Log('ConvertAddress').stream_handler("INFO")
        self._prepare()

    @staticmethod
    def _concat_sido_sgg(
        sido_nm: Optional[str],
        sgg_nm: Optional[str]
    ):
        if sido_nm is not None and sgg_nm is not None:
            return f'{sido_nm} {sgg_nm}'
        elif sido_nm is not None and sgg_nm is None:
            return sido_nm
        else:
            return None

    def _create_bjd_changed_dictionary(
        self,
        bjd_changed_df: pd.DataFrame
    ):
        bjd_changed_dictionary: Dict[str, str] = dict()
        for old_bjd_cd, old_bjd_nm, new_bjd_nm in zip(
            bjd_changed_df['법정동코드_변경전'],
            bjd_changed_df['법정동명_변경전'],
            bjd_changed_df['법정동명_변경후']
        ):
            if old_bjd_nm is not None \
            and new_bjd_nm is not None \
            and old_bjd_nm != new_bjd_nm \
            and old_bjd_nm not in self.bjd_current_bjd_nm_list \
            and str(old_bjd_cd)[5:] != '00000': # 시도, 시군구는 제외
                bjd_changed_dictionary[old_bjd_nm] = new_bjd_nm
        return bjd_changed_dictionary

    def _prepare(self):
        cls_bjd = Bjd()
        file_name_bjd: str = cls_bjd.file_name_bjd
        file_name_bjd_current: str = cls_bjd.file_name_bjd_current
        file_name_bjd_changed: str = cls_bjd.file_name_bjd_changed
        file_name_bjd_smallest: str = cls_bjd.file_name_bjd_smallest
        file_name_bjd_frequency_dictionary: str = cls_bjd.file_name_bjd_frequency_dictionary
        file_name_multiple_word_sgg_list: str = cls_bjd.file_name_multiple_word_sgg_list
        input_encoding = cls_bjd.output_encoding
        input_index = cls_bjd.output_index
        input_sep = cls_bjd.output_sep

        with open(file_name_bjd_current, 'r') as file_bjd_current:
            self.bjd_current_dic: Dict[str, str] = dict((line.split('\t')[2], line.split('\t')[9].replace('\n', '')) for line in file_bjd_current)

        with open(file_name_bjd_smallest, 'r') as file_bjd_smallest:
            self.bjd_smallest_list: List[str] = [line.strip() for line in file_bjd_smallest]

        with open(file_name_multiple_word_sgg_list, 'r') as file_multiple_word_sgg_list:
            self.multiple_word_sgg_list: List[str] = [line.strip() for line in file_multiple_word_sgg_list]

        bjd_df: pd.DataFrame = pd.read_csv(
            file_name_bjd,
            sep=input_sep,
            engine='python',
            encoding=input_encoding,
            dtype={
                '과거법정동코드': str,
                '법정동코드': str
            })
        self.bjd_df = bjd_df
        self.sido_list: List[str] = list(sido for sido in bjd_df['시도명'].unique() if isinstance(sido, str))
        self.sgg_list: List[str] = list(sgg for sgg in bjd_df['시군구명'].unique() if isinstance(sgg, str))
        self.emd_list: List[str] = list(emd for emd in bjd_df['읍면동명'].unique() if isinstance(emd, str))
        self.ri_list: List[str] = list(ri for ri in bjd_df['리명'].unique() if isinstance(ri, str))

        bjd_current_df: pd.DataFrame = pd.read_csv(
            file_name_bjd_current,
            sep=input_sep,
            engine='python',
            encoding=input_encoding)
        self.bjd_current_bjd_nm_list: List[str] = list(bjd_nm for bjd_nm in bjd_current_df['법정동명'] if bjd_nm is not None)
        bjd_current_df['시도시군구명'] = bjd_current_df[['시도명', '시군구명']].apply(lambda x: self._concat_sido_sgg(*x), axis=1)
        self.current_sido_sgg_list: List[str] = list(sido_sgg for sido_sgg in bjd_current_df['시도시군구명'].unique() if isinstance(sido_sgg, str))
        self.current_sido_list: List[str] = list(sido for sido in bjd_current_df['시도명'].unique() if isinstance(sido, str))
        self.current_sgg_list: List[str] = list(sgg for sgg in bjd_current_df['시군구명'].unique() if isinstance(sgg, str))
        self.current_emd_list: List[str] = list(emd for emd in bjd_current_df['읍면동명'].unique() if isinstance(emd, str))
        self.current_ri_list: List[str] = list(ri for ri in bjd_current_df['리명'].unique() if isinstance(ri, str))
        self.bjd_current_df = bjd_current_df

        bjd_changed_df: pd.DataFrame = pd.read_csv(
            file_name_bjd_changed,
            sep=input_sep,
            engine='python',
            encoding=input_encoding,
            dtype={
                '과거법정동코드': str,
                '법정동코드': str
            })
        sub_bjd_changed_df = bjd_changed_df.loc[
            (bjd_changed_df['법정동명_변경후'].isnull()==False) &
            (bjd_changed_df['법정동명_변경전'].isnull()==False)
        ]
        self.bjd_changed_dic: Dict[str, str] = self._create_bjd_changed_dictionary(sub_bjd_changed_df)
        self.bjd_changed_old_bjd_nm_list: List[str] = list(self.bjd_changed_dic.keys())

    @staticmethod
    def correct_simple_spacing(
        addr: str
    ) -> str:

        """
        입력된 문자열(한글 주소)의 연속된 공백을 단일 공백으로 정규화한 문자열로 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.

        Returns:
            str: A string that normalize multiple consecutive spaces in a string to a single space.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object('addr') must be string")

        return re.sub(r'\s+', ' ', addr)

    # 가장 작은 법정동명 뒤 번지가 띄어쓰기 없이 붙어있을 경우,
    # 가장 작은 법정동명에 포함된 숫자중 2자리수는 없음. 예 당산동1가, 을지로5가 등
    def correct_smallest_bjd_spacing(
        self,
        addr: str
    ) -> str:

        """
        입력된 문자열(한글 주소)의 가장 작은 법정동명과 번지 사이 빈공백을 단일 공백으로 정규화한 문자열로 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.
            ValueError: If the 'bjd_smallest_list' class constructor is None.

        Returns:
            str: A string that is the smallest administrative division name and address number space of the input string, with multiple spaces normalized to a single space.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object('addr') must be string")

        if self.bjd_smallest_list is None:
            raise ValueError("bjd_smallest_list is None")

        for bjdnm in self.bjd_smallest_list:
            if bjdnm in addr and (addr.split(bjdnm)[1][:2]).replace('-', '').isdigit() == True:
                addr = addr.split(bjdnm)[0] + bjdnm + ' ' + addr.split(bjdnm)[1]
                return addr
        return addr

    @staticmethod
    def union_similar_changed_bjd(
        changed_bjd_list: List[str]
    ):

        """
        교체할 변경내역 법정동 리스트 중 완전히 포함관계인 경우는 제외하여 반환
        """

        if len(changed_bjd_list) > 0:
            new_bjd_list: List[str] = list()
            for bjd in changed_bjd_list:
                if not any(bjd in other_bjd for other_bjd in changed_bjd_list if other_bjd != bjd):
                    new_bjd_list.append(bjd)
            return new_bjd_list
        else:
            return changed_bjd_list

    def correct_changed_bjd(
        self,
        addr: str,
        is_log: bool = True
    ) -> str:

        """
        입력된 문자열(한글 주소)에 변경전 법정동이 포함되어있으면 변경후 법정동명으로 교환하여 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.
            ValueError: If the 'bjd_changed_old_bjd_nm_list' class constructor is None.
            ValueError: If the 'bjd_changed_dic' class constructor is None.

        Returns:
            str: If the input string contains the previous administrative division name, eplace it with the modified administrative division name and return.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object('addr') must be string")

        if not isinstance(is_log, bool):
            raise TypeError("type of object('is_log') must be bool")

        if self.bjd_changed_old_bjd_nm_list is None:
            raise ValueError("bjd_changed_old_bjd_nm_list is None")

        if self.bjd_changed_dic is None:
            raise ValueError("bjd_changed_dic is None")

        origin_addr: str = addr
        changed_list: List[str] = list()
        for old_bjd_nm in self.bjd_changed_old_bjd_nm_list:
            if old_bjd_nm in addr:
                changed_list.append(old_bjd_nm)

        changed_list = self.union_similar_changed_bjd(changed_list)
        if changed_list:
            for changed_bjd_nm in changed_list:
                after_changed_bjd_nm = self.bjd_changed_dic[changed_bjd_nm]
                addr = addr.replace(changed_bjd_nm, after_changed_bjd_nm)
                if is_log:
                    self.logger.info(f'{origin_addr}')
                    self.logger.info(f'해당 법정동명은 변경되었습니다. 변경전 : [ {changed_bjd_nm} ] 변경후 : [ {after_changed_bjd_nm} ]')

        return addr

    def correct_bjd(
        self,
        addr: str,
        is_log: bool = True
    ):

        """
        입력된 문자열(한글 주소)의 법정동명 교정하여 반환

        Args:
            addr (str): The input korean address string.

        Raises:
            TypeError: If the 'addr' object is not of type string.

        Sub Functions:
            - correct_simple_spacing
            - correct_smallest_bjd_spacing
            - correct_changed_bjd

        Returns:
            Correct and return the input string by adjusting spaces in the main address and modifying the administrative division name.
        """

        if not isinstance(addr, str):
            raise TypeError("type of object('addr') must be string")

        if not isinstance(is_log, bool):
            raise TypeError("type of object('is_log') must be bool")

        addr = self.correct_simple_spacing(addr)
        addr = self.correct_smallest_bjd_spacing(addr)
        addr = self.correct_changed_bjd(addr, is_log)
        return addr