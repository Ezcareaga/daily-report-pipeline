#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Custom exceptions for the application."""


class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass


class DatabaseError(PipelineError):
    """Database connection or query errors."""
    pass

class ConfigurationError(PipelineError):
    """Configuration related errors."""
    pass