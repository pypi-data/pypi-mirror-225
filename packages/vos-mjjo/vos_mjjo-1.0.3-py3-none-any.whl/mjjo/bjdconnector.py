import pickle
import pkg_resources
import pandas as pd
from typing import (
    List,
    Dict,
    Optional
)
from dataclasses import dataclass
from mjjo.convaddr import ConvAddr


@dataclass
class BjdObject():

    CA = ConvAddr()
    current_sido_list = CA.sido_list
    current_sgg_list = CA.sgg_list
    current_emd_list = CA.emd_list
    current_ri_list = CA.ri_list
    multiple_word_sgg_list = CA.multiple_word_sgg_list

    def __init__(
        self,
        bjd_cd: str,
        full_bjd_nm: str
    ):
        self.bjd_cd: str = bjd_cd
        self.full_bjd_nm: str = full_bjd_nm
        self.typ: str = None
        self.sido: Optional[bool] = None
        self.sgg: Optional[bool] = None
        self.emd: Optional[bool] = None
        self.ri: Optional[bool] = None
        self.sido_nm: Optional[str] = None
        self.sgg_nm: Optional[str] = None
        self.emd_nm: Optional[str] = None
        self.ri_nm: Optional[str] = None
        self.sido_cd: Optional[str] = None
        self.sgg_cd: Optional[str] = None
        self.emd_cd: Optional[str] = None
        self.ri_cd: Optional[str] = None
        self.bjd_nm: str = None
        self._prepare()

    def _get_bjd_typ(
        self,
        bjd_nm
    ):
        for bjd_typ_nm, bjd_typ_group in [
            ("sido", self.current_sido_list),
            ("sgg", self.current_sgg_list),
            ("emd", self.current_emd_list),
            ("ri", self.current_ri_list)
        ]:
            if bjd_nm in bjd_typ_group:
                return bjd_typ_nm
        raise ValueError(f"{bjd_nm}: Invalid input")

    def _get_typ(self):
        if self.ri_nm is not None: return "ri"
        elif self.emd_nm is not None: return "emd"
        elif self.sgg_nm is not None: return "sgg"
        elif self.sido_nm is not None: return "sido"
        else: raise ValueError()

    def _get_bjd_nm(self):
        if self.typ == "sido": return self.sido_nm
        elif self.typ == "sgg": return self.sgg_nm
        elif self.typ == "emd": return self.emd_nm
        elif self.typ == "ri": return self.ri_nm
        else: raise ValueError()

    def _get_bjd_cd(self):
        if self.sido_nm is not None:
            if self.sido_nm == "세종특별자치시": self.sido_cd = self.bjd_cd[:5] + ("0" * 5)
            else: self.sido_cd = self.bjd_cd[:2] + ("0" * 8)
        if self.sgg_nm is not None:
            self.sgg_cd = self.bjd_cd[:5] + ("0" * 5)
        if self.emd_nm is not None:
            self.emd_cd = self.bjd_cd[:8] + ("0" * 2)
        if self.ri_nm is not None:
            self.ri_cd = self.bjd_cd

    def _get_is_existed_bjd(self):
        if self.sido_nm is not None:
            self.sido = True
        if self.sgg_nm is not None:
            self.sgg = True
        if self.emd_nm is not None:
            self.emd = True
        if self.ri_nm is not None:
            self.ri = True

    def _split_full_bjd_nm(self):
        for multiple_sgg_nm in self.multiple_word_sgg_list:
            if multiple_sgg_nm in self.full_bjd_nm:
                return [multiple_sgg_nm] + self.full_bjd_nm.replace(multiple_sgg_nm, "").split()
        return self.full_bjd_nm.split()

    def _prepare(self):
        bjd_nm_list = self._split_full_bjd_nm()
        for bjd_nm in bjd_nm_list:
            bjd_typ = self._get_bjd_typ(bjd_nm)
            if bjd_typ == "sido": self.sido_nm = bjd_nm
            elif bjd_typ == "sgg": self.sgg_nm = bjd_nm
            elif bjd_typ == "emd": self.emd_nm = bjd_nm
            elif bjd_typ == "ri": self.ri_nm = bjd_nm
            else: raise ValueError(f"{bjd_typ}: Invalid input")
        self.typ = self._get_typ()
        self.bjd_nm = self._get_bjd_nm()
        self._get_bjd_cd()
        self._get_is_existed_bjd()

    def _print(self):
        print(f"bjd_cd: {self.bjd_cd}")
        print(f"bjd_nm: {self.bjd_nm}")
        print(f"full_bjd_nm: {self.full_bjd_nm}")
        print(f"typ: {self.typ}")
        print(f"sido: {self.sido}")
        print(f"sgg: {self.sgg}")
        print(f"emd: {self.emd}")
        print(f"ri: {self.ri}")
        print(f"sido_nm: {self.sido_nm}")
        print(f"sgg_nm: {self.sgg_nm}")
        print(f"emd_nm: {self.emd_nm}")
        print(f"ri_nm: {self.ri_nm}")
        print(f"sido_cd: {self.sido_cd}")
        print(f"sgg_cd: {self.sgg_cd}")
        print(f"emd_cd: {self.emd_cd}")
        print(f"ri_cd: {self.ri_cd}")


@dataclass
class BjdConnector():

    bjd_top_relation = {
        "sido": None,
        "sgg": "sido",
        "emd": "sgg",
        "ri": "emd"
    }

    def __init__(
        self,
        bjd_cd: str,
        full_bjd_nm: str
    ):
        self.typ: str = None
        self.bjd_cd: str = bjd_cd
        self.bjd_nm: str = None
        self.full_bjd_nm: str = full_bjd_nm
        self.metadata: BjdObject() = None
        self.top_bjd_typ: Optional[str] = None
        self.top_bjd_cd: List[str] = []
        self.top_bjd_nm: List[str] = []
        self.top_bjd: List[BjdConnector()] = []
        self.bottom_bjd_cd: List[str] = []
        self.bottom_bjd_nm: List[str] = []
        self.bottom_bjd: List[BjdConnector()] = []
        self.is_smallest: bool = None
        self._update_metadata()
        self._update_top_bjd()

    def _update_metadata(self):
        bjd_object = BjdObject(
            bjd_cd=self.bjd_cd,
            full_bjd_nm=self.full_bjd_nm
        )
        self.metadata = bjd_object
        self.typ = bjd_object.typ
        self.bjd_nm = bjd_object.bjd_nm

    def _find_top_relation(
        self,
        typ,
        metadata
    ):
        if typ == "sido":
            return None
        top_typ = self.bjd_top_relation.get(typ)
        if getattr(metadata, f"{top_typ}") is True:
            return top_typ
        return self._find_top_relation(
            typ=top_typ,
            metadata=metadata
        ) # 상위 법정동이 없을 상위 법정동의 상위를 탐색

    def _update_top_bjd(self):
        typ = self.typ
        metadata = self.metadata
        self.top_bjd_typ = self._find_top_relation(
            typ=typ,
            metadata=metadata
        )
        if self.top_bjd_typ is not None:
            if self.top_bjd_typ == "sido":
                if self.metadata.sido_cd is not None:
                    self.top_bjd_nm.append(self.metadata.sido_nm)
                    self.top_bjd_cd.append(self.metadata.sido_cd)
                else:
                    print(self.metadata._print())
            if self.top_bjd_typ == "sgg":
                if self.metadata.sgg_cd is not None:
                    self.top_bjd_nm.append(self.metadata.sgg_nm)
                    self.top_bjd_cd.append(self.metadata.sgg_cd)
                else:
                    print(self.metadata._print())
            if self.top_bjd_typ == "emd":
                if self.metadata.emd_cd is not None:
                    self.top_bjd_nm.append(self.metadata.emd_nm)
                    self.top_bjd_cd.append(self.metadata.emd_cd)
                else:
                    print(self.metadata._print())

    def _update_connected_bjd(self):
        pass

    def _print(self):
        print(f"typ: {self.typ}")
        print(f"bjd_cd: {self.bjd_cd}")
        print(f"bjd_nm: {self.bjd_nm}")
        print(f"full_bjd_nm: {self.full_bjd_nm}")
        print(f"metadata: {self.metadata}")
        print(f"top_bjd_typ: {self.top_bjd_typ}")
        print(f"top_bjd_cd: {self.top_bjd_cd}")
        print(f"top_bjd_nm: {self.top_bjd_nm}")
        print(f"top_bjd: {self.top_bjd}")
        print(f"bottom_bjd_cd: {self.bottom_bjd_cd}")
        print(f"bottom_bjd_nm: {self.bottom_bjd_nm}")
        print(f"bottom_bjd: {self.bottom_bjd}")
        print(f"is_smallest: {self.is_smallest}")


@dataclass
class BjdConnectorGraph():

    CA = ConvAddr()
    bjd_current_df = CA.bjd_df

    def __init__(self):
        self.bjd_connectors: Dict[str, BjdConnector] = dict()
        self._creates_bjd_connectors()
        self._update_bjd_connectors()
        self._check_bjd_connectors_bottom_counts()

    def _creates_bjd_connectors(self):
        for _ in self.bjd_current_df[["법정동코드", "법정동명"]].itertuples():
            bjd_cd = str(_.법정동코드)
            full_bjd_nm =str(_.법정동명)

            self.bjd_connectors[bjd_cd] = BjdConnector(
                bjd_cd=bjd_cd,
                full_bjd_nm=full_bjd_nm
            )

    def _update_bjd_connectors(self):
        for bjd_cd, bjd_connector in self.bjd_connectors.items():
            if len(bjd_connector.top_bjd_cd):
                bjd_nm = bjd_connector.bjd_nm
                for top_bjd_cd in bjd_connector.top_bjd_cd:
                    if bjd_cd not in self.bjd_connectors[top_bjd_cd].bottom_bjd_cd:
                        self.bjd_connectors[top_bjd_cd].bottom_bjd_cd.append(bjd_cd)
                    if bjd_nm not in self.bjd_connectors[top_bjd_cd].bottom_bjd_nm:
                        self.bjd_connectors[top_bjd_cd].bottom_bjd_nm.append(bjd_nm)

        for bjd_cd, bjd_connector in self.bjd_connectors.items():
            if len(bjd_connector.top_bjd_cd) > 0:
                for top_bjd_cd in bjd_connector.top_bjd_cd:
                    bjd_connector.top_bjd.append(self.bjd_connectors[top_bjd_cd])
            if len(bjd_connector.bottom_bjd_cd) > 0:
                for bottom_bjd_cd in bjd_connector.bottom_bjd_cd:
                    bjd_connector.bottom_bjd.append(self.bjd_connectors[bottom_bjd_cd])

        for bjd_cd, bjd_connector in self.bjd_connectors.items():
            if len(bjd_connector.bottom_bjd_cd) == 0: bjd_connector.is_smallest = True
            else: bjd_connector.is_smallest = False

    def _check_bjd_connectors_bottom_counts(self):
        for bjd_cd, bjd_connector in self.bjd_connectors.items():
            if len(bjd_connector.bottom_bjd_cd) != len(bjd_connector.bottom_bjd):
                # bottom_bjd_nm 은 동일한 값이 있는경우가 있어서 제외
                # 4311132026 충청북도 청주시 상당구 미원면 기암리
                # 4311132033 충청북도 청주시 상당구 미원면 기암리
                raise ValueError(f"{bjd_cd}: Count of bottom values is not same")


@dataclass
class FullBjdConnector():

    CA = ConvAddr()
    BCG = BjdConnectorGraph()
    bjd_connectors = BCG.bjd_connectors
    multiple_word_sgg_list = CA.multiple_word_sgg_list

    def __init__(
        self,
        full_bjd_cd: str,
        full_bjd_nm: str,
        created_dt: str,
        deleted_dt: str,
        before_bjd_cd: str
    ):
        self.full_bjd_cd: str = full_bjd_cd
        self.full_bjd_nm: str = full_bjd_nm
        self.is_exist: bool = None
        self.created_dt: Optional[str] = created_dt
        self.deleted_dt: Optional[str] = deleted_dt
        self.before_bjd_cd: Optional[str] = before_bjd_cd
        self.before: List[FullBjdConnector] = []
        self.after: List[FullBjdConnector] = []
        self.is_smallest: bool = None
        self.sido: Optional[bool] = None
        self.sgg: Optional[bool] = None
        self.emd: Optional[bool] = None
        self.ri: Optional[bool] = None
        self.sido_nm: Optional[str] = None
        self.sgg_nm: Optional[str] = None
        self.emd_nm: Optional[str] = None
        self.ri_nm: Optional[str] = None
        self.sido_cd: Optional[str] = None
        self.sgg_cd: Optional[str] = None
        self.emd_cd: Optional[str] = None
        self.ri_cd: Optional[str] = None
        self.sido_bjd_connector: Optional[BjdConnector] = None
        self.sgg_bjd_connector: Optional[BjdConnector] = None
        self.emd_bjd_connector: Optional[BjdConnector] = None
        self.ri_bjd_connector: Optional[BjdConnector] = None
        self.is_exist = self._get_is_exist()
        self._get_bjd_connectors()

    def _split_full_bjd_nm(
        self
    ):
        if self.full_bjd_cd is not None:
            for multiple_sgg_nm in self.multiple_word_sgg_list:
                if multiple_sgg_nm in self.full_bjd_nm:
                    return [multiple_sgg_nm] + self.full_bjd_nm.replace(multiple_sgg_nm, "").split()
            return self.full_bjd_nm.split()
        return []

    def _get_is_exist(self):
        if self.deleted_dt is not None: return False
        return True

    def _get_bjd_cd_and_nm_from_typ(
        self, 
        bjd_connector
    ):
        typ = bjd_connector.typ
        setattr(self, f"{typ}", True)
        setattr(self, f"{typ}_cd", bjd_connector.bjd_cd)
        setattr(self, f"{typ}_nm", bjd_connector.bjd_nm)
        setattr(self, f"{typ}_bjd_connector", bjd_connector)

    def _get_each_bjd_connector(
        self,
        bjd_connector_list: List[BjdConnector], 
        full_bjd_nm_list: List[str]
    ):
        if len(bjd_connector_list) and len(full_bjd_nm_list):
            included_bjds = []
            for bjd_connector in bjd_connector_list:
                if bjd_connector.bjd_nm in full_bjd_nm_list:
                    included_bjds.append(bjd_connector.bjd_nm)
                    full_bjd_nm_list.remove(bjd_connector.bjd_nm)

                    self._get_bjd_cd_and_nm_from_typ(bjd_connector)
                    self._get_each_bjd_connector(
                        bjd_connector.top_bjd,
                        full_bjd_nm_list
                    )
            if len(included_bjds) == 0:
                raise ValueError(f"{[bjd_connector.bjd for bjd_connector in bjd_connector_list]}, Not in This Full Bjd Name List {full_bjd_nm_list}")

    def _get_bjd_connectors(self):
        full_bjd_nm_list = self._split_full_bjd_nm()
        start_bjd_connector = self.bjd_connectors[self.full_bjd_cd] # 가장 작은 단위의 법정동
        try:
            self._get_each_bjd_connector([start_bjd_connector], full_bjd_nm_list)
        except:
            print(f"Error Full Bjd Name List: {full_bjd_nm_list}, Bjd Code: {self.full_bjd_cd}")

    def _print(self):
        print(f"full_bjd_cd: {self.full_bjd_cd}")
        print(f"full_bjd_nm: {self.full_bjd_nm}")
        print(f"is_exist: {self.is_exist}")
        print(f"created_dt: {self.created_dt}")
        print(f"deleted_dt: {self.deleted_dt}")
        print(f"before: {self.before}")
        print(f"after: {self.after}")
        print(f"is_smallest: {self.is_smallest}")
        print(f"sido: {self.sido}")
        print(f"sgg: {self.sgg}")
        print(f"emd: {self.emd}")
        print(f"ri: {self.ri}")
        print(f"sido_nm: {self.sido_nm}")
        print(f"sgg_nm: {self.sgg_nm}")
        print(f"emd_nm: {self.emd_nm}")
        print(f"ri_nm: {self.ri_nm}")
        print(f"sido_cd: {self.sido_cd}")
        print(f"sgg_cd: {self.sgg_cd}")
        print(f"emd_cd: {self.emd_cd}")
        print(f"ri_cd: {self.ri_cd}")
        print(f"sido_bjd_connector: {self.sido_bjd_connector}")
        print(f"sgg_bjd_connector: {self.sgg_bjd_connector}")
        print(f"emd_bjd_connector: {self.emd_bjd_connector}")
        print(f"ri_bjd_connector: {self.ri_bjd_connector}")


@dataclass
class FullBjdGConnectorGraph():

    CA = ConvAddr()
    BCG = BjdConnectorGraph()
    bjd_df = CA.bjd_df
    bjd_connectors = BCG.bjd_connectors

    def __init__(self):
        self.full_bjd_connectors: Dict[str, FullBjdConnector] = dict()
        self._creates_full_bjd_connectors()
        self._update_before_and_after()

    @staticmethod
    def _replace_nan_with_none(df: pd.DataFrame):
        return df.where(pd.notna(df), None)

    def _creates_full_bjd_connectors(self):
        self.bjd_df = self.bjd_df[[
                "과거법정동코드",
                "법정동코드",
                "삭제일자",
                "생성일자",
                "법정동명"
            ]]
        self.bjd_df = self._replace_nan_with_none(self.bjd_df)
        for _ in self.bjd_df.itertuples():
            before_bjd_cd = str(_.과거법정동코드) if _.과거법정동코드 is not None else None
            full_bjd_cd = str(_.법정동코드) if _.법정동코드 is not None else None
            full_bjd_nm = str(_.법정동명) if _.법정동명 is not None else None
            created_dt = str(_.생성일자) if _.생성일자 is not None else None
            deleted_dt = str(_.삭제일자) if _.삭제일자 is not None else None

            self.full_bjd_connectors[full_bjd_cd] = FullBjdConnector(
                full_bjd_cd=full_bjd_cd,
                full_bjd_nm=full_bjd_nm,
                created_dt=created_dt,
                deleted_dt=deleted_dt,
                before_bjd_cd=before_bjd_cd
            )

    def _update_before_and_after(self):
        for bjd_cd, full_bjd_connector in self.full_bjd_connectors.items():
            if full_bjd_connector.before_bjd_cd is not None \
            and full_bjd_connector.before_bjd_cd in self.full_bjd_connectors.keys():
                self.full_bjd_connectors[bjd_cd].before.append(self.full_bjd_connectors[full_bjd_connector.before_bjd_cd])
                self.full_bjd_connectors[full_bjd_connector.before_bjd_cd].after.append(self.full_bjd_connectors[bjd_cd])


@dataclass
class ConvAddrByBjdConnector():

    bjd_connectors = None
    full_bjd_connectors = None
    file_name_bjd_connectors = pkg_resources.resource_filename(
        "mjjo", 
        "data/bjd_connectors.pkl"
    )
    file_name_full_bjd_connectors = pkg_resources.resource_filename(
        "mjjo", 
        "data/full_bjd_connectors.pkl"
    )


    @classmethod
    def load_data(cls):
        if cls.bjd_connectors is None:
            with open(cls.file_name_bjd_connectors, "rb") as f:
                cls.bjd_connectors = pickle.load(f)
                print("Done loaded bjd_connectors.pkl")
        if cls.full_bjd_connectors is None:
            with open(cls.file_name_full_bjd_connectors, "rb") as f:
                cls.full_bjd_connectors = pickle.load(f)
                print("Done loaded full_bjd_connectors.pkl")

    def __init__(self):
        self.load_data()

    def _get_bjd_connectors(
        self,
        addr: str,
        bjd_connector: BjdConnector
    ):
        if bjd_connector.is_smallest:
            return bjd_connector

        for bottom_bjd_connector in bjd_connector.bottom_bjd:
            if bottom_bjd_connector.bjd_nm in addr:
                result = self._get_bjd_connectors(addr, bottom_bjd_connector)
                if result is not None:
                    return result
        return None

    def _get_correct_bjd_connector(
        self,
        addr: str
    ):
        for bjd_connector in self.bjd_connectors.values():
            if bjd_connector.typ == 'sido' \
            and bjd_connector.bjd_nm in addr:
                return self._get_bjd_connectors(addr, bjd_connector)

    def _get_full_bjd_connector_by_bjd_connector(
        self,
        bjd_connector: BjdConnector
    ):
        return self.full_bjd_connectors[bjd_connector.bjd_cd]

    def _get_recently_full_bjd_connector(
        self,
        full_bjd_connector: FullBjdConnector
    ):
        if len(full_bjd_connector.after):
            if len(full_bjd_connector.after) > 1:
                print(f"{full_bjd_connector.after}가 복수개 존재합니다. 1번째 값을 이용합니다.")
            # print(f"{full_bjd_connector.full_bjd_nm} -> {full_bjd_connector.after[0].full_bjd_nm}")
            return self._get_recently_full_bjd_connector(full_bjd_connector.after[0])
        return full_bjd_connector

    def get_full_bjd_connector_by_address(
        self,
        addr: Optional[str]
    ):

        if not isinstance(addr, str):
            raise TypeError("type of object('addr') must be string")

        if addr is None:
            raise ValueError("addr is None")
            
        bjd_connector = self._get_correct_bjd_connector(addr)
        if bjd_connector is not None:
            full_bjd_connector = self._get_full_bjd_connector_by_bjd_connector(bjd_connector)
            full_bjd_connector = self._get_recently_full_bjd_connector(full_bjd_connector)
            return full_bjd_connector
        else:
            return None
