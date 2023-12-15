"""This module should load CVs from a given directory and split them up into chunks.

This should replace DirectoryLoader and RecursiveCharacterSplitter to split CVs more intelligently.
It is important to include metadata with the document chunks, especially email or name because this 
will be used to filter the documents to a single CV when using the vectorstore as a retriever.
This should make the cleaning obsolete since while we are chunking the CVs we will skip empty fields and urls. 
The expected output should be a list of document chunks with attached metadata.
"""

from typing import Iterable, Any
from itertools import chain

class CVSplitter:
    """Load CVs from a directory and divide content into chunks."""

    def __init__(self, lang: str = "no", fallback_lang: str | None = None) -> None:
        self.lang = lang
        self.fallback_lang = fallback_lang

    def get_lang_text(self, cv_component: dict[str, str] | None) -> str | None:
        if cv_component is None:
            return None
        if self.lang in cv_component:
            return cv_component[self.lang]
        if self.fallback_lang is not None and self.fallback_lang in cv_component:
            return cv_component[self.fallback_lang]
        return None

    def get_global_metadata(self, cv) -> dict[str, str]:
        """Return metadata that should be attached to all chunks from the CV."""
        meta = {
            "cv_id": cv["_id"],
            "user_id": cv["user_id"],
            "name": cv["name"],
            "email": cv["email"],
        }
        return meta

    def get_project_experiences(self, cv, global_meta) -> Iterable[str]:
        """Return project experiences as chunks with attached metadata."""
        for experience in cv["project_experiences"]:
            long_description = self.get_lang_text(experience["long_description"])
            if not long_description:
                continue
            components = ["Project experience:"]
            customer = self.get_lang_text(experience["customer"])
            if customer:
                components.append(f"Customer: {customer}")
            industry = self.get_lang_text(experience.get("industry"))
            if industry:
                components.append(f"Industry: {industry}")
            title = self.get_lang_text(experience["description"])
            if title:
                components.append(f"Title: {title}")
            components.append(long_description)
            if "project_experience_skills" in experience:
                components.append("\nProject experience skills:")
                skills = []
                for skill in experience["project_experience_skills"]:
                    s = self.get_lang_text(skill["tags"])
                    if s:
                        skills.append(s)
                components.append(", ".join(skills))
            if "roles" in experience:
                components.append("\nRoles:")
                for role in experience["roles"]:
                    name = self.get_lang_text(role.get("name"))
                    components.append(f"{name}")
                    long_description = self.get_lang_text(role["long_description"])
                    if long_description:
                        components.append(f"{long_description}\n")
            yield "\n".join(components), {
                **global_meta,
                "category": "project_experience",
            }

    def get_all_splits(self, cv):
        global_metas = self.get_global_metadata(cv)
        return chain(
            self.get_project_experiences(cv, global_metas),
            self.get_work_experiences(cv, global_metas),
        )
    
    def get_work_experiences(self, cv, global_meta) -> Iterable[str]:
        """Return work experiences as chunks with attached metadata."""
        for experience in cv["work_experiences"]:
            long_description = self.get_lang_text(experience["long_description"])
            if not long_description:
                continue
            components = ["Work Experience:"]
            employer = self.get_lang_text(experience["employer"])
            if employer:
                components.append(f"Employer: {employer}")
            title = self.get_lang_text(experience["description"])
            if title:
                components.append(f"Title: {title}")
            year_from = experience["year_from"]
            if year_from:
                components.append(f"Year_from: {year_from}")
            year_to = experience["year_to"]
            if year_to:
                components.append(f"Year_to: {year_to}")
            month_from = experience["month_from"]
            if month_from:
                components.append(f"Month_from: {month_from}")
            month_to = experience["month_to"]
            if month_to:
                components.append(f"Month_to: {month_to}")
            components.append(long_description)
            yield "\n".join(components), {
                **global_meta,
                "category": "work_experience",
            }


    def get_certifications(self, cv):
        """Return certifications as chunks with attached metadata."""
        pass

    def get_technologies(self, cv):
        """Return technologies as chunks with attached metadata."""
        pass

    def get_educations(self, cv):
        """Return educations as chunks with attached metadata."""
        pass


class CVCleaner:
    """Simple class for cleaning JSON objects by removing empty fields, urls and ids."""

    def prune(self, document: Any) -> Any:
        if isinstance(document, dict):
            return self.prune_dict(document)
        if isinstance(document, list):
            return self.prune_list(document)
        if isinstance(document, str):
            return self.prune_str(document)
        return document

    def prune_dict(self, document: dict) -> dict:
        pruned = {}
        for key, item in document.items():
            # Remove url and id fields
            if "url" in key or key.endswith(("_id")):
                continue
            item = self.prune(item)
            if not self.is_empty(item):
                pruned[key] = item
        return pruned

    def prune_list(self, document: list) -> list:
        pruned = []
        for item in document:
            item = self.prune(item)
            if not self.is_empty(item):
                pruned.append(item)
        return pruned

    def prune_str(self, document: str) -> str | None:
        if "https://" in document:  # Check to filter urls
            return None
        return document

    @staticmethod
    def is_empty(document: Any) -> bool:
        if document is None:
            return True
        if isinstance(document, (dict, list, str)):
            return len(document) == 0
        return False