from functools import wraps
from typing import Optional

from traceloop.semconv import SpanAttributes, TraceloopSpanKindValues
from traceloop.tracing.tracer import Tracer
from traceloop.utils import camel_to_snake


def task(
        name: Optional[str] = None,
        method_name: Optional[str] = None,
        tlp_span_kind: Optional[TraceloopSpanKindValues] = TraceloopSpanKindValues.TASK
):
    if method_name is None:
        return task_method(name=name, tlp_span_kind=tlp_span_kind)
    else:
        return task_class(name=name, method_name=method_name, tlp_span_kind=tlp_span_kind)


def task_method(name: Optional[str] = None,
                tlp_span_kind: Optional[TraceloopSpanKindValues] = TraceloopSpanKindValues.TASK):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            span_name = f"{name}.{tlp_span_kind.value}" if name else f"{fn.__name__}.{tlp_span_kind.value}"
            with Tracer.instance().start_as_current_span(span_name) as span:
                span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, tlp_span_kind.value)
                span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)
                return fn(*args, **kwargs)

        return wrap

    return decorate


def task_class(
        name: Optional[str],
        method_name: str,
        tlp_span_kind: Optional[TraceloopSpanKindValues] = TraceloopSpanKindValues.TASK
):
    def decorator(cls):
        task_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(cls, method_name, task_method(name=task_name, tlp_span_kind=tlp_span_kind)(method))
        return cls

    return decorator


def workflow(
        name: Optional[str] = None,
        method_name: Optional[str] = None,
        correlation_id: Optional[str] = None
):
    if method_name is None:
        return workflow_method(name=name, correlation_id=correlation_id)
    else:
        return workflow_class(name=name, method_name=method_name, correlation_id=correlation_id)


def workflow_method(name: Optional[str] = None, correlation_id: Optional[str] = None):
    def decorate(fn):
        @wraps(fn)
        def wrap(*args, **kwargs):
            Tracer.set_workflow_name(name or fn.__name__)
            span_name = f"{name}.workflow" if name else f"{fn.__name__}.workflow"
            with Tracer.instance().start_as_current_span(span_name) as span:
                span.set_attribute(SpanAttributes.TRACELOOP_SPAN_KIND, TraceloopSpanKindValues.WORKFLOW.value)
                span.set_attribute(SpanAttributes.TRACELOOP_ENTITY_NAME, name)

                if correlation_id:
                    span.set_attribute(SpanAttributes.TRACELOOP_CORRELATION_ID, correlation_id)
                return fn(*args, **kwargs)

        return wrap

    return decorate


def workflow_class(name: Optional[str], method_name: str, correlation_id: Optional[str] = None):
    def decorator(cls):
        workflow_name = name if name else camel_to_snake(cls.__name__)
        method = getattr(cls, method_name)
        setattr(cls, method_name, workflow_method(name=workflow_name, correlation_id=correlation_id)(method))
        return cls

    return decorator


def agent(name: Optional[str] = None, method_name: Optional[str] = None):
    return task(name=name, method_name=method_name, tlp_span_kind=TraceloopSpanKindValues.AGENT)


def tool(name: Optional[str] = None, method_name: Optional[str] = None):
    return task(name=name, method_name=method_name, tlp_span_kind=TraceloopSpanKindValues.TOOL)
