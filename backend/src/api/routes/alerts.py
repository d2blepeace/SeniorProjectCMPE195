"""
Alert management endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List

from backend.src.storage import db_manager
from backend.src.storage.models import Alert, AlertCreate
from backend.src.utils.logger import logger

router = APIRouter()
