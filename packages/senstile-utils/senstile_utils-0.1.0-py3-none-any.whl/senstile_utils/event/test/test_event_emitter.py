import pytest
from senstile_utils.event import EventEmitter, EventEmitterException


def test_subscribe():
    emitter = EventEmitter()

    def callback(topic, data):
        assert topic == "test_topic"
        assert data == "test_data"

    emitter.subscribe("test_topic", callback)
    assert "test_topic" in emitter.subscriptions
    assert callback in emitter.subscriptions["test_topic"]


def test_emit():
    emitter = EventEmitter()
    received = []

    def callback(topic, data):
        received.append((topic, data))

    emitter.subscribe("test_topic", callback)
    emitter.emit("test_topic", "test_data")

    assert received == [("test_topic", "test_data")]


def test_unsubscribe():
    emitter = EventEmitter()

    def callback(topic, data):
        pass

    subscription = emitter.subscribe("test_topic", callback)
    subscription.unsubscribe()

    assert callback not in emitter.subscriptions["test_topic"]


def test_emit_exception():
    emitter = EventEmitter()
    with pytest.raises(EventEmitterException, match="There is not such a topic"):
        emitter.emit("non_existent_topic", "test_data")


def test_validate_topic_exception():
    emitter = EventEmitter()
    with pytest.raises(EventEmitterException, match="Topic is required"):
        emitter.subscribe("", lambda x, y: None)


def test_validate_callback_exception():
    emitter = EventEmitter()
    with pytest.raises(EventEmitterException, match="Callable is required"):
        emitter.subscribe("test_topic", None)


## More Complex stuff

def test_multiple_subscriptions_single_topic():
    emitter = EventEmitter()
    received = []
    
    def callback1(topic, data):
        received.append((topic, data))
        
    def callback2(topic, data):
        received.append((topic, data))
    
    emitter.subscribe("test_topic", callback1)
    emitter.subscribe("test_topic", callback2)
    emitter.emit("test_topic", "test_data")
    
    assert received == [("test_topic", "test_data"), ("test_topic", "test_data")]

def test_multiple_topics_and_subscriptions():
    emitter = EventEmitter()
    results = []
    
    def callback1(topic, data):
        results.append((1, topic, data))
        
    def callback2(topic, data):
        results.append((2, topic, data))
        
    emitter.subscribe("topic1", callback1)
    emitter.subscribe("topic2", callback2)
    emitter.emit("topic1", "data1")
    emitter.emit("topic2", "data2")
    
    assert results == [(1, "topic1", "data1"), (2, "topic2", "data2")]

def test_unsubscribe_from_topic_with_multiple_subscribers():
    emitter = EventEmitter()
    received = []
    
    def callback1(topic, data):
        received.append((topic, data))
        
    def callback2(topic, data):
        received.append((topic, data))
    
    sub1 = emitter.subscribe("test_topic", callback1)
    sub2 = emitter.subscribe("test_topic", callback2)
    
    sub1.unsubscribe()
    emitter.emit("test_topic", "test_data")
    
    assert received == [("test_topic", "test_data")]

def test_exception_in_one_callback():
    emitter = EventEmitter()
    received = []
    
    def callback1(topic, data):
        raise Exception("Error in callback1")
        received.append((topic, data))
        
    def callback2(topic, data):
        received.append((topic, data))
    
    emitter.subscribe("test_topic", callback1)
    emitter.subscribe("test_topic", callback2)
    emitter.emit("test_topic", "test_data")
    
    assert received == [("test_topic", "test_data")]

def test_unsubscribe_inside_a_callback():
    emitter = EventEmitter()
    received = []
    
    def callback1(topic, data):
        received.append((topic, data))
        sub1.unsubscribe()
        
    def callback2(topic, data):
        received.append((topic, data))
    
    sub1 = emitter.subscribe("test_topic", callback1)
    sub2 = emitter.subscribe("test_topic", callback2)
    emitter.emit("test_topic", "test_data1")
    emitter.emit("test_topic", "test_data2")
    
    assert received == [("test_topic", "test_data1"), ("test_topic", "test_data1"), ("test_topic", "test_data2")]
