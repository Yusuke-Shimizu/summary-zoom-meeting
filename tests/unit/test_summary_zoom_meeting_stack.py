import aws_cdk as core
import aws_cdk.assertions as assertions

from summary_zoom_meeting.summary_zoom_meeting_stack import SummaryZoomMeetingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in summary_zoom_meeting/summary_zoom_meeting_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SummaryZoomMeetingStack(app, "summary-zoom-meeting")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
