"""Standard response models for the API"""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    """Standard API response format"""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Human-readable message")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response format"""
    success: bool = Field(default=False, description="Always false for errors")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(default=None, description="Machine-readable error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")


class StatusResponse(BaseModel):
    """Health check and status response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Status check timestamp")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional status details")


class JobResponse(BaseModel):
    """Response for background job operations"""
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(..., description="Job status")
    created_at: datetime = Field(..., description="Job creation time")
    message: str = Field(..., description="Job status message")
    progress: Optional[int] = Field(default=None, description="Job progress percentage")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")
