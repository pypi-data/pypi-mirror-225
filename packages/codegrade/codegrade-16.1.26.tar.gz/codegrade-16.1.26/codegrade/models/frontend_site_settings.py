"""The module that defines the ``FrontendSiteSettings`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import datetime
import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa
from cg_maybe import Maybe, Nothing
from cg_maybe.utils import maybe_from_nullable

from .. import parsers
from ..utils import to_dict
from .fraction import Fraction


@dataclass
class FrontendSiteSettings:
    """The JSON representation of options visible to all users."""

    #: The default amount of time a step/substep in AutoTest can run. This can
    #: be overridden by the teacher.
    auto_test_max_time_command: Maybe["datetime.timedelta"] = Nothing
    #: Default message for IO Test steps of an AutoTest.
    auto_test_io_test_message: Maybe["str"] = Nothing
    #: Default message for IO Test sub-steps of an AutoTest.
    auto_test_io_test_sub_message: Maybe["str"] = Nothing
    #: Default message for Run Program steps of an AutoTest.
    auto_test_run_program_message: Maybe["str"] = Nothing
    #: Default message for Capture Points steps of an AutoTest.
    auto_test_capture_points_message: Maybe["str"] = Nothing
    #: Default message for Checkpoint steps of an AutoTest.
    auto_test_checkpoint_message: Maybe["str"] = Nothing
    #: Default message for Unit Test steps of an AutoTest.
    auto_test_unit_test_message: Maybe["str"] = Nothing
    #: Default message for Code Quality steps of an AutoTest.
    auto_test_code_quality_message: Maybe["str"] = Nothing
    #: The IDs of the currently recent base images for AutoTest 2.0. These are
    #: the images that we want users to use for new AutoTest 2.0
    #: configurations. Make sure that if you add something to this list it is
    #: also added to NEW\_AUTO\_TEST\_ALLOWED\_INITIAL\_BUILD\_IDS, as
    #: otherwise the user is not allowed to use the image. The last item in
    #: this list will be the default image id.
    new_auto_test_current_initial_build_ids: Maybe["t.Sequence[str]"] = Nothing
    #: The maximum time a command may run in the build part of AutoTest 2.0.
    new_auto_test_build_max_command_time: Maybe["datetime.timedelta"] = Nothing
    #: The maximum time a command may run in the test part of AutoTest 2.0.
    #: This is also the default value for timeout steps.
    new_auto_test_test_max_command_time: Maybe["datetime.timedelta"] = Nothing
    #: The maximum time-delta an exam may take. Increasing this value also
    #: increases the maximum amount of time the login tokens send via email are
    #: valid. Therefore, you should make this too long.
    exam_login_max_length: Maybe["datetime.timedelta"] = Nothing
    #: This determines how long before the exam we will send the login emails
    #: to the students (only when enabled of course).
    login_token_before_time: Maybe["t.Sequence[datetime.timedelta]"] = Nothing
    #: The amount of time a reset token is valid. You should not increase this
    #: value too much as users might be not be too careful with these tokens.
    #: Increasing this value will allow **all** existing tokens to live longer.
    reset_token_time: Maybe["datetime.timedelta"] = Nothing
    #: The email shown to users as the email of CodeGrade.
    site_email: Maybe["str"] = Nothing
    #: The maximum amount of lines that we should in render in one go. If a
    #: file contains more lines than this we will show a warning asking the
    #: user what to do.
    max_lines: Maybe["int"] = Nothing
    #: The amount of time to wait between two consecutive polls to see if a
    #: user has new notifications. Setting this value too low will cause
    #: unnecessary stress on the server.
    notification_poll_time: Maybe["datetime.timedelta"] = Nothing
    #: What is the maximum amount of time after a release a message should be
    #: shown on the HomeGrid. **Note**: this is the amount of time after the
    #: release, not after this instance has been upgraded to this release.
    release_message_max_time: Maybe["datetime.timedelta"] = Nothing
    #: The maximum amount of matches of a plagiarism run that we will store. If
    #: there are more matches than this they will be discarded.
    max_plagiarism_matches: Maybe["int"] = Nothing
    #: The maximum amount of time that the global setup script in AutoTest may
    #: take. If it takes longer than this it will be killed and the run will
    #: fail.
    auto_test_max_global_setup_time: Maybe["datetime.timedelta"] = Nothing
    #: The maximum amount of time that the per student setup script in AutoTest
    #: may take. If it takes longer than this it will be killed and the result
    #: of the student will be in the state "timed-out".
    auto_test_max_per_student_setup_time: Maybe["datetime.timedelta"] = Nothing
    #: The default value for the grading scale of new assignments.
    assignment_default_grading_scale: Maybe[
        "t.Literal['percentage', 'points']"
    ] = Nothing
    #: The default points grading scale points of new assignments.
    assignment_default_grading_scale_points: Maybe["Fraction"] = Nothing
    #: If enabled teachers are allowed to bulk upload submissions (and create
    #: users) using a zip file in a format created by Blackboard.
    blackboard_zip_upload_enabled: Maybe["bool"] = Nothing
    #: If enabled teachers can use rubrics on CodeGrade. Disabling this feature
    #: will not delete existing rubrics.
    rubrics_enabled: Maybe["bool"] = Nothing
    #: If enabled teachers can view rubrics on the submissions list page. Here
    #: they have the student view version of the rubric as apposed to the
    #: editor view in the manage assignment page.
    rubric_enabled_for_teacher_on_submissions_page: Maybe["bool"] = Nothing
    #: Currently unused.
    automatic_lti_role_enabled: Maybe["bool"] = Nothing
    #: Should LTI be enabled.
    lti_enabled: Maybe["bool"] = Nothing
    #: Should linters be enabled.
    linters_enabled: Maybe["bool"] = Nothing
    #: Should rubrics be submitted incrementally, so if a user selects a item
    #: should this be automatically be submitted to the server, or should it
    #: only be possible to submit a complete rubric at once. This feature is
    #: useless if rubrics is not set to true.
    incremental_rubric_submission_enabled: Maybe["bool"] = Nothing
    #: Should it be possible to register on the website. This makes it possible
    #: for any body to register an account on the website.
    register_enabled: Maybe["bool"] = Nothing
    #: Should group assignments be enabled.
    groups_enabled: Maybe["bool"] = Nothing
    #: Should auto test be enabled.
    auto_test_enabled: Maybe["bool"] = Nothing
    #: Should it be possible for teachers to create links that users can use to
    #: register in a course. Links to enroll can be created even if this
    #: feature is disabled.
    course_register_enabled: Maybe["bool"] = Nothing
    #: Should it be possible to render html files within CodeGrade. This opens
    #: up more attack surfaces as it is now possible by design for students to
    #: run javascript. This is all done in a sandboxed iframe but still.
    render_html_enabled: Maybe["bool"] = Nothing
    #: Should it be possible to email students.
    email_students_enabled: Maybe["bool"] = Nothing
    #: Should peer feedback be enabled.
    peer_feedback_enabled: Maybe["bool"] = Nothing
    #: Should AT image caching be enabled.
    at_image_caching_enabled: Maybe["bool"] = Nothing
    #: Should it be possible to let students pay for a course. Please note that
    #: to enable this deploy config needs to be updated, so don't just enable
    #: it.
    student_payment_enabled: Maybe["bool"] = Nothing
    #: Can students submit using the online editor.
    editor_enabled: Maybe["bool"] = Nothing
    #: Can AutoTest configurations be created and run using the 2.0
    #: infrastructure.
    new_auto_test_enabled: Maybe["bool"] = Nothing
    #: Whether the time as detected locally on a user's computer is corrected
    #: by the difference with the time as reported by the backend server.
    server_time_correction_enabled: Maybe["bool"] = Nothing
    #: Whether the gathering of user behaviour events and subsequent metrics
    #: enabled.
    metric_gathering_enabled: Maybe["bool"] = Nothing
    #: Whether teachers have access to the assignment manager - notifications
    #: panel, which gives control over when to send notifications to graders to
    #: finish their job, and also allows teachers to provide email(s) to notify
    #: when all graders are finished.
    grading_notifications_enabled: Maybe["bool"] = Nothing
    #: Feedback threads will start collapsed from this depth of the tree.
    feedback_threads_initially_collapsed: Maybe["int"] = Nothing
    #: The time interval between gathering of metrics.
    metric_gathering_time_interval: Maybe["datetime.timedelta"] = Nothing
    #: The percentage of the event buffer fill that causes a gathering of
    #: metrics.
    metric_gathering_event_interval: Maybe["int"] = Nothing
    #: The size of the circular buffer containing the trace of user behaviour
    #: events.
    metric_event_buffer_size: Maybe["int"] = Nothing
    #: The total time limit for evaluating a single metric.
    metric_evaluation_time_limit: Maybe["datetime.timedelta"] = Nothing
    #: The time before we yield to the event loop during evaluation of a
    #: metric.
    metric_evaluation_time_chunk_size: Maybe["datetime.timedelta"] = Nothing
    #: Expressions for the metrics we want to measure.
    metric_gathering_expressions: Maybe["t.Mapping[str, str]"] = Nothing
    #: The maximum amount of difference between the server time and the local
    #: time before we consider the local time to be out of sync with our
    #: servers.
    server_time_diff_tolerance: Maybe["datetime.timedelta"] = Nothing
    #: The interval at which we request the server time in case it is out of
    #: sync with the local time.
    server_time_sync_interval: Maybe["datetime.timedelta"] = Nothing
    #: Whether the is\_admin global permission should be enabled. Users with a
    #: global role with this permission automatically get all permissions,
    #: everywhere. Users with a tenant role with this permission automatically
    #: get all permissions within their tenant.
    is_admin_permission_enabled: Maybe["bool"] = Nothing
    #: The interval of time in milliseconds between each search of the starting
    #: element of a tour once the component trigger is found and visible.
    tour_polling_interval: Maybe["int"] = Nothing
    #: The interval of time in milliseconds between each search for the
    #: anchoring elements of a tour step on the DOM.
    find_element_interval: Maybe["int"] = Nothing
    #: The maximum number of tries while searching for the anchoring elements
    #: of a tour step on the DOM.
    find_element_max_tries: Maybe["int"] = Nothing
    #: Tour Configurations for enabled components. For each tour a name, a
    #: component trigger, and a starting trigger need to be specified. Tour
    #: Names must be unique, and each tour can contain an arbitrary number of
    #: steps.
    tour_configurations: Maybe["t.Sequence[t.Any]"] = Nothing
    #: Number of decimals for percentage-based grades in assignments, this also
    #: determines which decimal position the grade is rounded to.
    assignment_percentage_decimals: Maybe["int"] = Nothing
    #: Number of decimals for point-based grades in assignments, this also
    #: determines which decimal position the grade is rounded to.
    assignment_point_decimals: Maybe["int"] = Nothing
    #: How many lines of output we will still animate using the collapseable
    #: body in ATv2 output viewer.
    output_viewer_animation_limit_lines_count: Maybe["int"] = Nothing
    #: Should the lock date be copied from the LMS through LTI, or should we
    #: allow the user to set it in CodeGrade.
    lti_lock_date_copying_enabled: Maybe["bool"] = Nothing
    #: Whether the Max Points field within the assignment general settings is
    #: enabled. If disabled, teachers will not be able to award extra points
    #: for assignments.
    assignment_max_points_enabled: Maybe["bool"] = Nothing
    #: Whether the gradebook on the course management page is enabled.
    course_gradebook_enabled: Maybe["bool"] = Nothing
    #: Wether the description on the assignment management page is enabled.
    assignment_description_enabled: Maybe["bool"] = Nothing
    #: The minimum size of a gradebook before we show a warning that there are
    #: so many entries in the gradebook that it may slow down rendering or
    #: crash the page.
    course_gradebook_render_warning_size: Maybe["int"] = Nothing
    #: Whether it is possible for teachers to create links for batches of users
    #: that can be used to register in a course. Links to enroll can be created
    #: even if this feature is disabled.
    course_bulk_register_enabled: Maybe["bool"] = Nothing
    #: The file size above which users will be shown a warning that parsing the
    #: file might cause a slow down in their browser.
    csv_large_file_limit: Maybe["int"] = Nothing
    #: The amount of errors that occur above which we will ask the user to make
    #: sure that the given file is actually a CSV.
    csv_too_many_errors_limit: Maybe["int"] = Nothing
    #: Whether AutoTest 2.0 configuration importing from other assignments is
    #: enabled.
    new_auto_test_copying_enabled: Maybe["bool"] = Nothing
    #: Whether it should be possible to set the maximum scale points for an
    #: assignment using point-based scale. This is different from the
    #: assignment max grade and can not be used with percentage-based scales.
    assignment_grading_scale_points_enabled: Maybe["bool"] = Nothing
    #: The maximum age a submission can be before we do not retry subscribing
    #: to its result if it cannot be found the first time.
    new_auto_test_old_submission_age: Maybe["datetime.timedelta"] = Nothing
    #: Should course id form Canvas be copied through LTI(1.3), and stored in
    #: our database or not.
    canvas_course_id_copying_enabled: Maybe["bool"] = Nothing
    #: Can teacher edit their students' work through the code editor.
    editor_enabled_for_teachers: Maybe["bool"] = Nothing
    #: Whether the test submission is copied over when importing an assignment.
    test_submission_copying_on_import_enabled: Maybe["bool"] = Nothing
    #: Whether the diff viewer should be shown in AutoTest v2 IO Test steps.
    new_auto_test_diff_viewer_enabled: Maybe["bool"] = Nothing
    #: Whether assignment importing is done in stages, where we first select
    #: course.
    staged_assignment_importer_enabled: Maybe["bool"] = Nothing
    #: Whether to show the sections the users are a part of in the submission
    #: list. This also applies to groups.
    sections_in_submission_list_enabled: Maybe["bool"] = Nothing
    #: Whether to allow teachers to provide an URL of a GitHub repo, to be
    #: forked by the students when they setup a new repository via the GitHub
    #: integration.
    github_template_repo_enabled: Maybe["bool"] = Nothing
    #: Whether the community library is enabled and available.
    community_library: Maybe["bool"] = Nothing
    #: Whether it is possible to publish new items to the community library.
    #: This feature only has effect when `COMMUNITY_LIBRARY` is enabled too.
    community_library_publishing: Maybe["bool"] = Nothing
    #: Whether exporting plagiarism reports as PDF is enabled.
    plagiarism_pdf_export_enabled: Maybe["bool"] = Nothing
    #: Whether bulk export of plagiarism reports is enabled.
    plagiarism_bulk_export_enabled: Maybe["bool"] = Nothing
    #: The maximum amount of plagiarism cases that can be exported at a time.
    plagiarism_bulk_export_max_cases: Maybe["int"] = Nothing
    #: Whether quality comments generated by code editor ATv2 runs should be
    #: displayed in the editor.
    quality_comments_in_code_editor: Maybe["bool"] = Nothing
    #: Whether during an SSO launch new user are granted their global role
    #: based on the SSO launch data.
    sso_infer_global_staff_role: Maybe["bool"] = Nothing

    raw_data: t.Optional[t.Dict[str, t.Any]] = field(init=False, repr=False)

    data_parser: t.ClassVar = rqa.Lazy(
        lambda: rqa.FixedMapping(
            rqa.OptionalArgument(
                "AUTO_TEST_MAX_TIME_COMMAND",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The default amount of time a step/substep in AutoTest can"
                    " run. This can be overridden by the teacher."
                ),
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_IO_TEST_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for IO Test steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_IO_TEST_SUB_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for IO Test sub-steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_RUN_PROGRAM_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Run Program steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_CAPTURE_POINTS_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Capture Points steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_CHECKPOINT_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Checkpoint steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_UNIT_TEST_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Unit Test steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_CODE_QUALITY_MESSAGE",
                rqa.SimpleValue.str,
                doc="Default message for Code Quality steps of an AutoTest.",
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_CURRENT_INITIAL_BUILD_IDS",
                rqa.List(rqa.SimpleValue.str),
                doc=(
                    "The IDs of the currently recent base images for AutoTest"
                    " 2.0. These are the images that we want users to use for"
                    " new AutoTest 2.0 configurations. Make sure that if you"
                    " add something to this list it is also added to"
                    " NEW\\_AUTO\\_TEST\\_ALLOWED\\_INITIAL\\_BUILD\\_IDS, as"
                    " otherwise the user is not allowed to use the image. The"
                    " last item in this list will be the default image id."
                ),
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_BUILD_MAX_COMMAND_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum time a command may run in the build part of"
                    " AutoTest 2.0."
                ),
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_TEST_MAX_COMMAND_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum time a command may run in the test part of"
                    " AutoTest 2.0. This is also the default value for timeout"
                    " steps."
                ),
            ),
            rqa.OptionalArgument(
                "EXAM_LOGIN_MAX_LENGTH",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum time-delta an exam may take. Increasing this"
                    " value also increases the maximum amount of time the"
                    " login tokens send via email are valid. Therefore, you"
                    " should make this too long."
                ),
            ),
            rqa.OptionalArgument(
                "LOGIN_TOKEN_BEFORE_TIME",
                rqa.List(rqa.RichValue.TimeDelta),
                doc=(
                    "This determines how long before the exam we will send the"
                    " login emails to the students (only when enabled of"
                    " course)."
                ),
            ),
            rqa.OptionalArgument(
                "RESET_TOKEN_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The amount of time a reset token is valid. You should not"
                    " increase this value too much as users might be not be"
                    " too careful with these tokens. Increasing this value"
                    " will allow **all** existing tokens to live longer."
                ),
            ),
            rqa.OptionalArgument(
                "SITE_EMAIL",
                rqa.SimpleValue.str,
                doc="The email shown to users as the email of CodeGrade.",
            ),
            rqa.OptionalArgument(
                "MAX_LINES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum amount of lines that we should in render in"
                    " one go. If a file contains more lines than this we will"
                    " show a warning asking the user what to do."
                ),
            ),
            rqa.OptionalArgument(
                "NOTIFICATION_POLL_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The amount of time to wait between two consecutive polls"
                    " to see if a user has new notifications. Setting this"
                    " value too low will cause unnecessary stress on the"
                    " server."
                ),
            ),
            rqa.OptionalArgument(
                "RELEASE_MESSAGE_MAX_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "What is the maximum amount of time after a release a"
                    " message should be shown on the HomeGrid. **Note**: this"
                    " is the amount of time after the release, not after this"
                    " instance has been upgraded to this release."
                ),
            ),
            rqa.OptionalArgument(
                "MAX_PLAGIARISM_MATCHES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum amount of matches of a plagiarism run that we"
                    " will store. If there are more matches than this they"
                    " will be discarded."
                ),
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_MAX_GLOBAL_SETUP_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum amount of time that the global setup script"
                    " in AutoTest may take. If it takes longer than this it"
                    " will be killed and the run will fail."
                ),
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum amount of time that the per student setup"
                    " script in AutoTest may take. If it takes longer than"
                    " this it will be killed and the result of the student"
                    ' will be in the state "timed-out".'
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_DEFAULT_GRADING_SCALE",
                rqa.StringEnum("percentage", "points"),
                doc=(
                    "The default value for the grading scale of new"
                    " assignments."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_DEFAULT_GRADING_SCALE_POINTS",
                parsers.ParserFor.make(Fraction),
                doc=(
                    "The default points grading scale points of new"
                    " assignments."
                ),
            ),
            rqa.OptionalArgument(
                "BLACKBOARD_ZIP_UPLOAD_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "If enabled teachers are allowed to bulk upload"
                    " submissions (and create users) using a zip file in a"
                    " format created by Blackboard."
                ),
            ),
            rqa.OptionalArgument(
                "RUBRICS_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "If enabled teachers can use rubrics on CodeGrade."
                    " Disabling this feature will not delete existing rubrics."
                ),
            ),
            rqa.OptionalArgument(
                "RUBRIC_ENABLED_FOR_TEACHER_ON_SUBMISSIONS_PAGE",
                rqa.SimpleValue.bool,
                doc=(
                    "If enabled teachers can view rubrics on the submissions"
                    " list page. Here they have the student view version of"
                    " the rubric as apposed to the editor view in the manage"
                    " assignment page."
                ),
            ),
            rqa.OptionalArgument(
                "AUTOMATIC_LTI_ROLE_ENABLED",
                rqa.SimpleValue.bool,
                doc="Currently unused.",
            ),
            rqa.OptionalArgument(
                "LTI_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should LTI be enabled.",
            ),
            rqa.OptionalArgument(
                "LINTERS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should linters be enabled.",
            ),
            rqa.OptionalArgument(
                "INCREMENTAL_RUBRIC_SUBMISSION_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should rubrics be submitted incrementally, so if a user"
                    " selects a item should this be automatically be submitted"
                    " to the server, or should it only be possible to submit a"
                    " complete rubric at once. This feature is useless if"
                    " rubrics is not set to true."
                ),
            ),
            rqa.OptionalArgument(
                "REGISTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible to register on the website. This"
                    " makes it possible for any body to register an account on"
                    " the website."
                ),
            ),
            rqa.OptionalArgument(
                "GROUPS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should group assignments be enabled.",
            ),
            rqa.OptionalArgument(
                "AUTO_TEST_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should auto test be enabled.",
            ),
            rqa.OptionalArgument(
                "COURSE_REGISTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible for teachers to create links that"
                    " users can use to register in a course. Links to enroll"
                    " can be created even if this feature is disabled."
                ),
            ),
            rqa.OptionalArgument(
                "RENDER_HTML_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible to render html files within"
                    " CodeGrade. This opens up more attack surfaces as it is"
                    " now possible by design for students to run javascript."
                    " This is all done in a sandboxed iframe but still."
                ),
            ),
            rqa.OptionalArgument(
                "EMAIL_STUDENTS_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should it be possible to email students.",
            ),
            rqa.OptionalArgument(
                "PEER_FEEDBACK_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should peer feedback be enabled.",
            ),
            rqa.OptionalArgument(
                "AT_IMAGE_CACHING_ENABLED",
                rqa.SimpleValue.bool,
                doc="Should AT image caching be enabled.",
            ),
            rqa.OptionalArgument(
                "STUDENT_PAYMENT_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should it be possible to let students pay for a course."
                    " Please note that to enable this deploy config needs to"
                    " be updated, so don't just enable it."
                ),
            ),
            rqa.OptionalArgument(
                "EDITOR_ENABLED",
                rqa.SimpleValue.bool,
                doc="Can students submit using the online editor.",
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Can AutoTest configurations be created and run using the"
                    " 2.0 infrastructure."
                ),
            ),
            rqa.OptionalArgument(
                "SERVER_TIME_CORRECTION_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the time as detected locally on a user's computer"
                    " is corrected by the difference with the time as reported"
                    " by the backend server."
                ),
            ),
            rqa.OptionalArgument(
                "METRIC_GATHERING_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the gathering of user behaviour events and"
                    " subsequent metrics enabled."
                ),
            ),
            rqa.OptionalArgument(
                "GRADING_NOTIFICATIONS_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether teachers have access to the assignment manager -"
                    " notifications panel, which gives control over when to"
                    " send notifications to graders to finish their job, and"
                    " also allows teachers to provide email(s) to notify when"
                    " all graders are finished."
                ),
            ),
            rqa.OptionalArgument(
                "FEEDBACK_THREADS_INITIALLY_COLLAPSED",
                rqa.SimpleValue.int,
                doc=(
                    "Feedback threads will start collapsed from this depth of"
                    " the tree."
                ),
            ),
            rqa.OptionalArgument(
                "METRIC_GATHERING_TIME_INTERVAL",
                rqa.RichValue.TimeDelta,
                doc="The time interval between gathering of metrics.",
            ),
            rqa.OptionalArgument(
                "METRIC_GATHERING_EVENT_INTERVAL",
                rqa.SimpleValue.int,
                doc=(
                    "The percentage of the event buffer fill that causes a"
                    " gathering of metrics."
                ),
            ),
            rqa.OptionalArgument(
                "METRIC_EVENT_BUFFER_SIZE",
                rqa.SimpleValue.int,
                doc=(
                    "The size of the circular buffer containing the trace of"
                    " user behaviour events."
                ),
            ),
            rqa.OptionalArgument(
                "METRIC_EVALUATION_TIME_LIMIT",
                rqa.RichValue.TimeDelta,
                doc="The total time limit for evaluating a single metric.",
            ),
            rqa.OptionalArgument(
                "METRIC_EVALUATION_TIME_CHUNK_SIZE",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The time before we yield to the event loop during"
                    " evaluation of a metric."
                ),
            ),
            rqa.OptionalArgument(
                "METRIC_GATHERING_EXPRESSIONS",
                rqa.LookupMapping(rqa.SimpleValue.str),
                doc="Expressions for the metrics we want to measure.",
            ),
            rqa.OptionalArgument(
                "SERVER_TIME_DIFF_TOLERANCE",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum amount of difference between the server time"
                    " and the local time before we consider the local time to"
                    " be out of sync with our servers."
                ),
            ),
            rqa.OptionalArgument(
                "SERVER_TIME_SYNC_INTERVAL",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The interval at which we request the server time in case"
                    " it is out of sync with the local time."
                ),
            ),
            rqa.OptionalArgument(
                "IS_ADMIN_PERMISSION_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the is\\_admin global permission should be"
                    " enabled. Users with a global role with this permission"
                    " automatically get all permissions, everywhere. Users"
                    " with a tenant role with this permission automatically"
                    " get all permissions within their tenant."
                ),
            ),
            rqa.OptionalArgument(
                "TOUR_POLLING_INTERVAL",
                rqa.SimpleValue.int,
                doc=(
                    "The interval of time in milliseconds between each search"
                    " of the starting element of a tour once the component"
                    " trigger is found and visible."
                ),
            ),
            rqa.OptionalArgument(
                "FIND_ELEMENT_INTERVAL",
                rqa.SimpleValue.int,
                doc=(
                    "The interval of time in milliseconds between each search"
                    " for the anchoring elements of a tour step on the DOM."
                ),
            ),
            rqa.OptionalArgument(
                "FIND_ELEMENT_MAX_TRIES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum number of tries while searching for the"
                    " anchoring elements of a tour step on the DOM."
                ),
            ),
            rqa.OptionalArgument(
                "TOUR_CONFIGURATIONS",
                rqa.List(rqa.AnyValue),
                doc=(
                    "Tour Configurations for enabled components. For each tour"
                    " a name, a component trigger, and a starting trigger need"
                    " to be specified. Tour Names must be unique, and each"
                    " tour can contain an arbitrary number of steps."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_PERCENTAGE_DECIMALS",
                rqa.SimpleValue.int,
                doc=(
                    "Number of decimals for percentage-based grades in"
                    " assignments, this also determines which decimal position"
                    " the grade is rounded to."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_POINT_DECIMALS",
                rqa.SimpleValue.int,
                doc=(
                    "Number of decimals for point-based grades in assignments,"
                    " this also determines which decimal position the grade is"
                    " rounded to."
                ),
            ),
            rqa.OptionalArgument(
                "OUTPUT_VIEWER_ANIMATION_LIMIT_LINES_COUNT",
                rqa.SimpleValue.int,
                doc=(
                    "How many lines of output we will still animate using the"
                    " collapseable body in ATv2 output viewer."
                ),
            ),
            rqa.OptionalArgument(
                "LTI_LOCK_DATE_COPYING_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should the lock date be copied from the LMS through LTI,"
                    " or should we allow the user to set it in CodeGrade."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_MAX_POINTS_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the Max Points field within the assignment"
                    " general settings is enabled. If disabled, teachers will"
                    " not be able to award extra points for assignments."
                ),
            ),
            rqa.OptionalArgument(
                "COURSE_GRADEBOOK_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the gradebook on the course management page is"
                    " enabled."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_DESCRIPTION_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Wether the description on the assignment management page"
                    " is enabled."
                ),
            ),
            rqa.OptionalArgument(
                "COURSE_GRADEBOOK_RENDER_WARNING_SIZE",
                rqa.SimpleValue.int,
                doc=(
                    "The minimum size of a gradebook before we show a warning"
                    " that there are so many entries in the gradebook that it"
                    " may slow down rendering or crash the page."
                ),
            ),
            rqa.OptionalArgument(
                "COURSE_BULK_REGISTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether it is possible for teachers to create links for"
                    " batches of users that can be used to register in a"
                    " course. Links to enroll can be created even if this"
                    " feature is disabled."
                ),
            ),
            rqa.OptionalArgument(
                "CSV_LARGE_FILE_LIMIT",
                rqa.SimpleValue.int,
                doc=(
                    "The file size above which users will be shown a warning"
                    " that parsing the file might cause a slow down in their"
                    " browser."
                ),
            ),
            rqa.OptionalArgument(
                "CSV_TOO_MANY_ERRORS_LIMIT",
                rqa.SimpleValue.int,
                doc=(
                    "The amount of errors that occur above which we will ask"
                    " the user to make sure that the given file is actually a"
                    " CSV."
                ),
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_COPYING_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether AutoTest 2.0 configuration importing from other"
                    " assignments is enabled."
                ),
            ),
            rqa.OptionalArgument(
                "ASSIGNMENT_GRADING_SCALE_POINTS_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether it should be possible to set the maximum scale"
                    " points for an assignment using point-based scale. This"
                    " is different from the assignment max grade and can not"
                    " be used with percentage-based scales."
                ),
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_OLD_SUBMISSION_AGE",
                rqa.RichValue.TimeDelta,
                doc=(
                    "The maximum age a submission can be before we do not"
                    " retry subscribing to its result if it cannot be found"
                    " the first time."
                ),
            ),
            rqa.OptionalArgument(
                "CANVAS_COURSE_ID_COPYING_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Should course id form Canvas be copied through LTI(1.3),"
                    " and stored in our database or not."
                ),
            ),
            rqa.OptionalArgument(
                "EDITOR_ENABLED_FOR_TEACHERS",
                rqa.SimpleValue.bool,
                doc=(
                    "Can teacher edit their students' work through the code"
                    " editor."
                ),
            ),
            rqa.OptionalArgument(
                "TEST_SUBMISSION_COPYING_ON_IMPORT_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the test submission is copied over when importing"
                    " an assignment."
                ),
            ),
            rqa.OptionalArgument(
                "NEW_AUTO_TEST_DIFF_VIEWER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether the diff viewer should be shown in AutoTest v2 IO"
                    " Test steps."
                ),
            ),
            rqa.OptionalArgument(
                "STAGED_ASSIGNMENT_IMPORTER_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether assignment importing is done in stages, where we"
                    " first select course."
                ),
            ),
            rqa.OptionalArgument(
                "SECTIONS_IN_SUBMISSION_LIST_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether to show the sections the users are a part of in"
                    " the submission list. This also applies to groups."
                ),
            ),
            rqa.OptionalArgument(
                "GITHUB_TEMPLATE_REPO_ENABLED",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether to allow teachers to provide an URL of a GitHub"
                    " repo, to be forked by the students when they setup a new"
                    " repository via the GitHub integration."
                ),
            ),
            rqa.OptionalArgument(
                "COMMUNITY_LIBRARY",
                rqa.SimpleValue.bool,
                doc="Whether the community library is enabled and available.",
            ),
            rqa.OptionalArgument(
                "COMMUNITY_LIBRARY_PUBLISHING",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether it is possible to publish new items to the"
                    " community library. This feature only has effect when"
                    " `COMMUNITY_LIBRARY` is enabled too."
                ),
            ),
            rqa.OptionalArgument(
                "PLAGIARISM_PDF_EXPORT_ENABLED",
                rqa.SimpleValue.bool,
                doc="Whether exporting plagiarism reports as PDF is enabled.",
            ),
            rqa.OptionalArgument(
                "PLAGIARISM_BULK_EXPORT_ENABLED",
                rqa.SimpleValue.bool,
                doc="Whether bulk export of plagiarism reports is enabled.",
            ),
            rqa.OptionalArgument(
                "PLAGIARISM_BULK_EXPORT_MAX_CASES",
                rqa.SimpleValue.int,
                doc=(
                    "The maximum amount of plagiarism cases that can be"
                    " exported at a time."
                ),
            ),
            rqa.OptionalArgument(
                "QUALITY_COMMENTS_IN_CODE_EDITOR",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether quality comments generated by code editor ATv2"
                    " runs should be displayed in the editor."
                ),
            ),
            rqa.OptionalArgument(
                "SSO_INFER_GLOBAL_STAFF_ROLE",
                rqa.SimpleValue.bool,
                doc=(
                    "Whether during an SSO launch new user are granted their"
                    " global role based on the SSO launch data."
                ),
            ),
        ).use_readable_describe(True)
    )

    def __post_init__(self) -> None:
        getattr(super(), "__post_init__", lambda: None)()
        self.auto_test_max_time_command = maybe_from_nullable(
            self.auto_test_max_time_command
        )
        self.auto_test_io_test_message = maybe_from_nullable(
            self.auto_test_io_test_message
        )
        self.auto_test_io_test_sub_message = maybe_from_nullable(
            self.auto_test_io_test_sub_message
        )
        self.auto_test_run_program_message = maybe_from_nullable(
            self.auto_test_run_program_message
        )
        self.auto_test_capture_points_message = maybe_from_nullable(
            self.auto_test_capture_points_message
        )
        self.auto_test_checkpoint_message = maybe_from_nullable(
            self.auto_test_checkpoint_message
        )
        self.auto_test_unit_test_message = maybe_from_nullable(
            self.auto_test_unit_test_message
        )
        self.auto_test_code_quality_message = maybe_from_nullable(
            self.auto_test_code_quality_message
        )
        self.new_auto_test_current_initial_build_ids = maybe_from_nullable(
            self.new_auto_test_current_initial_build_ids
        )
        self.new_auto_test_build_max_command_time = maybe_from_nullable(
            self.new_auto_test_build_max_command_time
        )
        self.new_auto_test_test_max_command_time = maybe_from_nullable(
            self.new_auto_test_test_max_command_time
        )
        self.exam_login_max_length = maybe_from_nullable(
            self.exam_login_max_length
        )
        self.login_token_before_time = maybe_from_nullable(
            self.login_token_before_time
        )
        self.reset_token_time = maybe_from_nullable(self.reset_token_time)
        self.site_email = maybe_from_nullable(self.site_email)
        self.max_lines = maybe_from_nullable(self.max_lines)
        self.notification_poll_time = maybe_from_nullable(
            self.notification_poll_time
        )
        self.release_message_max_time = maybe_from_nullable(
            self.release_message_max_time
        )
        self.max_plagiarism_matches = maybe_from_nullable(
            self.max_plagiarism_matches
        )
        self.auto_test_max_global_setup_time = maybe_from_nullable(
            self.auto_test_max_global_setup_time
        )
        self.auto_test_max_per_student_setup_time = maybe_from_nullable(
            self.auto_test_max_per_student_setup_time
        )
        self.assignment_default_grading_scale = maybe_from_nullable(
            self.assignment_default_grading_scale
        )
        self.assignment_default_grading_scale_points = maybe_from_nullable(
            self.assignment_default_grading_scale_points
        )
        self.blackboard_zip_upload_enabled = maybe_from_nullable(
            self.blackboard_zip_upload_enabled
        )
        self.rubrics_enabled = maybe_from_nullable(self.rubrics_enabled)
        self.rubric_enabled_for_teacher_on_submissions_page = (
            maybe_from_nullable(
                self.rubric_enabled_for_teacher_on_submissions_page
            )
        )
        self.automatic_lti_role_enabled = maybe_from_nullable(
            self.automatic_lti_role_enabled
        )
        self.lti_enabled = maybe_from_nullable(self.lti_enabled)
        self.linters_enabled = maybe_from_nullable(self.linters_enabled)
        self.incremental_rubric_submission_enabled = maybe_from_nullable(
            self.incremental_rubric_submission_enabled
        )
        self.register_enabled = maybe_from_nullable(self.register_enabled)
        self.groups_enabled = maybe_from_nullable(self.groups_enabled)
        self.auto_test_enabled = maybe_from_nullable(self.auto_test_enabled)
        self.course_register_enabled = maybe_from_nullable(
            self.course_register_enabled
        )
        self.render_html_enabled = maybe_from_nullable(
            self.render_html_enabled
        )
        self.email_students_enabled = maybe_from_nullable(
            self.email_students_enabled
        )
        self.peer_feedback_enabled = maybe_from_nullable(
            self.peer_feedback_enabled
        )
        self.at_image_caching_enabled = maybe_from_nullable(
            self.at_image_caching_enabled
        )
        self.student_payment_enabled = maybe_from_nullable(
            self.student_payment_enabled
        )
        self.editor_enabled = maybe_from_nullable(self.editor_enabled)
        self.new_auto_test_enabled = maybe_from_nullable(
            self.new_auto_test_enabled
        )
        self.server_time_correction_enabled = maybe_from_nullable(
            self.server_time_correction_enabled
        )
        self.metric_gathering_enabled = maybe_from_nullable(
            self.metric_gathering_enabled
        )
        self.grading_notifications_enabled = maybe_from_nullable(
            self.grading_notifications_enabled
        )
        self.feedback_threads_initially_collapsed = maybe_from_nullable(
            self.feedback_threads_initially_collapsed
        )
        self.metric_gathering_time_interval = maybe_from_nullable(
            self.metric_gathering_time_interval
        )
        self.metric_gathering_event_interval = maybe_from_nullable(
            self.metric_gathering_event_interval
        )
        self.metric_event_buffer_size = maybe_from_nullable(
            self.metric_event_buffer_size
        )
        self.metric_evaluation_time_limit = maybe_from_nullable(
            self.metric_evaluation_time_limit
        )
        self.metric_evaluation_time_chunk_size = maybe_from_nullable(
            self.metric_evaluation_time_chunk_size
        )
        self.metric_gathering_expressions = maybe_from_nullable(
            self.metric_gathering_expressions
        )
        self.server_time_diff_tolerance = maybe_from_nullable(
            self.server_time_diff_tolerance
        )
        self.server_time_sync_interval = maybe_from_nullable(
            self.server_time_sync_interval
        )
        self.is_admin_permission_enabled = maybe_from_nullable(
            self.is_admin_permission_enabled
        )
        self.tour_polling_interval = maybe_from_nullable(
            self.tour_polling_interval
        )
        self.find_element_interval = maybe_from_nullable(
            self.find_element_interval
        )
        self.find_element_max_tries = maybe_from_nullable(
            self.find_element_max_tries
        )
        self.tour_configurations = maybe_from_nullable(
            self.tour_configurations
        )
        self.assignment_percentage_decimals = maybe_from_nullable(
            self.assignment_percentage_decimals
        )
        self.assignment_point_decimals = maybe_from_nullable(
            self.assignment_point_decimals
        )
        self.output_viewer_animation_limit_lines_count = maybe_from_nullable(
            self.output_viewer_animation_limit_lines_count
        )
        self.lti_lock_date_copying_enabled = maybe_from_nullable(
            self.lti_lock_date_copying_enabled
        )
        self.assignment_max_points_enabled = maybe_from_nullable(
            self.assignment_max_points_enabled
        )
        self.course_gradebook_enabled = maybe_from_nullable(
            self.course_gradebook_enabled
        )
        self.assignment_description_enabled = maybe_from_nullable(
            self.assignment_description_enabled
        )
        self.course_gradebook_render_warning_size = maybe_from_nullable(
            self.course_gradebook_render_warning_size
        )
        self.course_bulk_register_enabled = maybe_from_nullable(
            self.course_bulk_register_enabled
        )
        self.csv_large_file_limit = maybe_from_nullable(
            self.csv_large_file_limit
        )
        self.csv_too_many_errors_limit = maybe_from_nullable(
            self.csv_too_many_errors_limit
        )
        self.new_auto_test_copying_enabled = maybe_from_nullable(
            self.new_auto_test_copying_enabled
        )
        self.assignment_grading_scale_points_enabled = maybe_from_nullable(
            self.assignment_grading_scale_points_enabled
        )
        self.new_auto_test_old_submission_age = maybe_from_nullable(
            self.new_auto_test_old_submission_age
        )
        self.canvas_course_id_copying_enabled = maybe_from_nullable(
            self.canvas_course_id_copying_enabled
        )
        self.editor_enabled_for_teachers = maybe_from_nullable(
            self.editor_enabled_for_teachers
        )
        self.test_submission_copying_on_import_enabled = maybe_from_nullable(
            self.test_submission_copying_on_import_enabled
        )
        self.new_auto_test_diff_viewer_enabled = maybe_from_nullable(
            self.new_auto_test_diff_viewer_enabled
        )
        self.staged_assignment_importer_enabled = maybe_from_nullable(
            self.staged_assignment_importer_enabled
        )
        self.sections_in_submission_list_enabled = maybe_from_nullable(
            self.sections_in_submission_list_enabled
        )
        self.github_template_repo_enabled = maybe_from_nullable(
            self.github_template_repo_enabled
        )
        self.community_library = maybe_from_nullable(self.community_library)
        self.community_library_publishing = maybe_from_nullable(
            self.community_library_publishing
        )
        self.plagiarism_pdf_export_enabled = maybe_from_nullable(
            self.plagiarism_pdf_export_enabled
        )
        self.plagiarism_bulk_export_enabled = maybe_from_nullable(
            self.plagiarism_bulk_export_enabled
        )
        self.plagiarism_bulk_export_max_cases = maybe_from_nullable(
            self.plagiarism_bulk_export_max_cases
        )
        self.quality_comments_in_code_editor = maybe_from_nullable(
            self.quality_comments_in_code_editor
        )
        self.sso_infer_global_staff_role = maybe_from_nullable(
            self.sso_infer_global_staff_role
        )

    def to_dict(self) -> t.Dict[str, t.Any]:
        res: t.Dict[str, t.Any] = {}
        if self.auto_test_max_time_command.is_just:
            res["AUTO_TEST_MAX_TIME_COMMAND"] = to_dict(
                self.auto_test_max_time_command.value
            )
        if self.auto_test_io_test_message.is_just:
            res["AUTO_TEST_IO_TEST_MESSAGE"] = to_dict(
                self.auto_test_io_test_message.value
            )
        if self.auto_test_io_test_sub_message.is_just:
            res["AUTO_TEST_IO_TEST_SUB_MESSAGE"] = to_dict(
                self.auto_test_io_test_sub_message.value
            )
        if self.auto_test_run_program_message.is_just:
            res["AUTO_TEST_RUN_PROGRAM_MESSAGE"] = to_dict(
                self.auto_test_run_program_message.value
            )
        if self.auto_test_capture_points_message.is_just:
            res["AUTO_TEST_CAPTURE_POINTS_MESSAGE"] = to_dict(
                self.auto_test_capture_points_message.value
            )
        if self.auto_test_checkpoint_message.is_just:
            res["AUTO_TEST_CHECKPOINT_MESSAGE"] = to_dict(
                self.auto_test_checkpoint_message.value
            )
        if self.auto_test_unit_test_message.is_just:
            res["AUTO_TEST_UNIT_TEST_MESSAGE"] = to_dict(
                self.auto_test_unit_test_message.value
            )
        if self.auto_test_code_quality_message.is_just:
            res["AUTO_TEST_CODE_QUALITY_MESSAGE"] = to_dict(
                self.auto_test_code_quality_message.value
            )
        if self.new_auto_test_current_initial_build_ids.is_just:
            res["NEW_AUTO_TEST_CURRENT_INITIAL_BUILD_IDS"] = to_dict(
                self.new_auto_test_current_initial_build_ids.value
            )
        if self.new_auto_test_build_max_command_time.is_just:
            res["NEW_AUTO_TEST_BUILD_MAX_COMMAND_TIME"] = to_dict(
                self.new_auto_test_build_max_command_time.value
            )
        if self.new_auto_test_test_max_command_time.is_just:
            res["NEW_AUTO_TEST_TEST_MAX_COMMAND_TIME"] = to_dict(
                self.new_auto_test_test_max_command_time.value
            )
        if self.exam_login_max_length.is_just:
            res["EXAM_LOGIN_MAX_LENGTH"] = to_dict(
                self.exam_login_max_length.value
            )
        if self.login_token_before_time.is_just:
            res["LOGIN_TOKEN_BEFORE_TIME"] = to_dict(
                self.login_token_before_time.value
            )
        if self.reset_token_time.is_just:
            res["RESET_TOKEN_TIME"] = to_dict(self.reset_token_time.value)
        if self.site_email.is_just:
            res["SITE_EMAIL"] = to_dict(self.site_email.value)
        if self.max_lines.is_just:
            res["MAX_LINES"] = to_dict(self.max_lines.value)
        if self.notification_poll_time.is_just:
            res["NOTIFICATION_POLL_TIME"] = to_dict(
                self.notification_poll_time.value
            )
        if self.release_message_max_time.is_just:
            res["RELEASE_MESSAGE_MAX_TIME"] = to_dict(
                self.release_message_max_time.value
            )
        if self.max_plagiarism_matches.is_just:
            res["MAX_PLAGIARISM_MATCHES"] = to_dict(
                self.max_plagiarism_matches.value
            )
        if self.auto_test_max_global_setup_time.is_just:
            res["AUTO_TEST_MAX_GLOBAL_SETUP_TIME"] = to_dict(
                self.auto_test_max_global_setup_time.value
            )
        if self.auto_test_max_per_student_setup_time.is_just:
            res["AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME"] = to_dict(
                self.auto_test_max_per_student_setup_time.value
            )
        if self.assignment_default_grading_scale.is_just:
            res["ASSIGNMENT_DEFAULT_GRADING_SCALE"] = to_dict(
                self.assignment_default_grading_scale.value
            )
        if self.assignment_default_grading_scale_points.is_just:
            res["ASSIGNMENT_DEFAULT_GRADING_SCALE_POINTS"] = to_dict(
                self.assignment_default_grading_scale_points.value
            )
        if self.blackboard_zip_upload_enabled.is_just:
            res["BLACKBOARD_ZIP_UPLOAD_ENABLED"] = to_dict(
                self.blackboard_zip_upload_enabled.value
            )
        if self.rubrics_enabled.is_just:
            res["RUBRICS_ENABLED"] = to_dict(self.rubrics_enabled.value)
        if self.rubric_enabled_for_teacher_on_submissions_page.is_just:
            res["RUBRIC_ENABLED_FOR_TEACHER_ON_SUBMISSIONS_PAGE"] = to_dict(
                self.rubric_enabled_for_teacher_on_submissions_page.value
            )
        if self.automatic_lti_role_enabled.is_just:
            res["AUTOMATIC_LTI_ROLE_ENABLED"] = to_dict(
                self.automatic_lti_role_enabled.value
            )
        if self.lti_enabled.is_just:
            res["LTI_ENABLED"] = to_dict(self.lti_enabled.value)
        if self.linters_enabled.is_just:
            res["LINTERS_ENABLED"] = to_dict(self.linters_enabled.value)
        if self.incremental_rubric_submission_enabled.is_just:
            res["INCREMENTAL_RUBRIC_SUBMISSION_ENABLED"] = to_dict(
                self.incremental_rubric_submission_enabled.value
            )
        if self.register_enabled.is_just:
            res["REGISTER_ENABLED"] = to_dict(self.register_enabled.value)
        if self.groups_enabled.is_just:
            res["GROUPS_ENABLED"] = to_dict(self.groups_enabled.value)
        if self.auto_test_enabled.is_just:
            res["AUTO_TEST_ENABLED"] = to_dict(self.auto_test_enabled.value)
        if self.course_register_enabled.is_just:
            res["COURSE_REGISTER_ENABLED"] = to_dict(
                self.course_register_enabled.value
            )
        if self.render_html_enabled.is_just:
            res["RENDER_HTML_ENABLED"] = to_dict(
                self.render_html_enabled.value
            )
        if self.email_students_enabled.is_just:
            res["EMAIL_STUDENTS_ENABLED"] = to_dict(
                self.email_students_enabled.value
            )
        if self.peer_feedback_enabled.is_just:
            res["PEER_FEEDBACK_ENABLED"] = to_dict(
                self.peer_feedback_enabled.value
            )
        if self.at_image_caching_enabled.is_just:
            res["AT_IMAGE_CACHING_ENABLED"] = to_dict(
                self.at_image_caching_enabled.value
            )
        if self.student_payment_enabled.is_just:
            res["STUDENT_PAYMENT_ENABLED"] = to_dict(
                self.student_payment_enabled.value
            )
        if self.editor_enabled.is_just:
            res["EDITOR_ENABLED"] = to_dict(self.editor_enabled.value)
        if self.new_auto_test_enabled.is_just:
            res["NEW_AUTO_TEST_ENABLED"] = to_dict(
                self.new_auto_test_enabled.value
            )
        if self.server_time_correction_enabled.is_just:
            res["SERVER_TIME_CORRECTION_ENABLED"] = to_dict(
                self.server_time_correction_enabled.value
            )
        if self.metric_gathering_enabled.is_just:
            res["METRIC_GATHERING_ENABLED"] = to_dict(
                self.metric_gathering_enabled.value
            )
        if self.grading_notifications_enabled.is_just:
            res["GRADING_NOTIFICATIONS_ENABLED"] = to_dict(
                self.grading_notifications_enabled.value
            )
        if self.feedback_threads_initially_collapsed.is_just:
            res["FEEDBACK_THREADS_INITIALLY_COLLAPSED"] = to_dict(
                self.feedback_threads_initially_collapsed.value
            )
        if self.metric_gathering_time_interval.is_just:
            res["METRIC_GATHERING_TIME_INTERVAL"] = to_dict(
                self.metric_gathering_time_interval.value
            )
        if self.metric_gathering_event_interval.is_just:
            res["METRIC_GATHERING_EVENT_INTERVAL"] = to_dict(
                self.metric_gathering_event_interval.value
            )
        if self.metric_event_buffer_size.is_just:
            res["METRIC_EVENT_BUFFER_SIZE"] = to_dict(
                self.metric_event_buffer_size.value
            )
        if self.metric_evaluation_time_limit.is_just:
            res["METRIC_EVALUATION_TIME_LIMIT"] = to_dict(
                self.metric_evaluation_time_limit.value
            )
        if self.metric_evaluation_time_chunk_size.is_just:
            res["METRIC_EVALUATION_TIME_CHUNK_SIZE"] = to_dict(
                self.metric_evaluation_time_chunk_size.value
            )
        if self.metric_gathering_expressions.is_just:
            res["METRIC_GATHERING_EXPRESSIONS"] = to_dict(
                self.metric_gathering_expressions.value
            )
        if self.server_time_diff_tolerance.is_just:
            res["SERVER_TIME_DIFF_TOLERANCE"] = to_dict(
                self.server_time_diff_tolerance.value
            )
        if self.server_time_sync_interval.is_just:
            res["SERVER_TIME_SYNC_INTERVAL"] = to_dict(
                self.server_time_sync_interval.value
            )
        if self.is_admin_permission_enabled.is_just:
            res["IS_ADMIN_PERMISSION_ENABLED"] = to_dict(
                self.is_admin_permission_enabled.value
            )
        if self.tour_polling_interval.is_just:
            res["TOUR_POLLING_INTERVAL"] = to_dict(
                self.tour_polling_interval.value
            )
        if self.find_element_interval.is_just:
            res["FIND_ELEMENT_INTERVAL"] = to_dict(
                self.find_element_interval.value
            )
        if self.find_element_max_tries.is_just:
            res["FIND_ELEMENT_MAX_TRIES"] = to_dict(
                self.find_element_max_tries.value
            )
        if self.tour_configurations.is_just:
            res["TOUR_CONFIGURATIONS"] = to_dict(
                self.tour_configurations.value
            )
        if self.assignment_percentage_decimals.is_just:
            res["ASSIGNMENT_PERCENTAGE_DECIMALS"] = to_dict(
                self.assignment_percentage_decimals.value
            )
        if self.assignment_point_decimals.is_just:
            res["ASSIGNMENT_POINT_DECIMALS"] = to_dict(
                self.assignment_point_decimals.value
            )
        if self.output_viewer_animation_limit_lines_count.is_just:
            res["OUTPUT_VIEWER_ANIMATION_LIMIT_LINES_COUNT"] = to_dict(
                self.output_viewer_animation_limit_lines_count.value
            )
        if self.lti_lock_date_copying_enabled.is_just:
            res["LTI_LOCK_DATE_COPYING_ENABLED"] = to_dict(
                self.lti_lock_date_copying_enabled.value
            )
        if self.assignment_max_points_enabled.is_just:
            res["ASSIGNMENT_MAX_POINTS_ENABLED"] = to_dict(
                self.assignment_max_points_enabled.value
            )
        if self.course_gradebook_enabled.is_just:
            res["COURSE_GRADEBOOK_ENABLED"] = to_dict(
                self.course_gradebook_enabled.value
            )
        if self.assignment_description_enabled.is_just:
            res["ASSIGNMENT_DESCRIPTION_ENABLED"] = to_dict(
                self.assignment_description_enabled.value
            )
        if self.course_gradebook_render_warning_size.is_just:
            res["COURSE_GRADEBOOK_RENDER_WARNING_SIZE"] = to_dict(
                self.course_gradebook_render_warning_size.value
            )
        if self.course_bulk_register_enabled.is_just:
            res["COURSE_BULK_REGISTER_ENABLED"] = to_dict(
                self.course_bulk_register_enabled.value
            )
        if self.csv_large_file_limit.is_just:
            res["CSV_LARGE_FILE_LIMIT"] = to_dict(
                self.csv_large_file_limit.value
            )
        if self.csv_too_many_errors_limit.is_just:
            res["CSV_TOO_MANY_ERRORS_LIMIT"] = to_dict(
                self.csv_too_many_errors_limit.value
            )
        if self.new_auto_test_copying_enabled.is_just:
            res["NEW_AUTO_TEST_COPYING_ENABLED"] = to_dict(
                self.new_auto_test_copying_enabled.value
            )
        if self.assignment_grading_scale_points_enabled.is_just:
            res["ASSIGNMENT_GRADING_SCALE_POINTS_ENABLED"] = to_dict(
                self.assignment_grading_scale_points_enabled.value
            )
        if self.new_auto_test_old_submission_age.is_just:
            res["NEW_AUTO_TEST_OLD_SUBMISSION_AGE"] = to_dict(
                self.new_auto_test_old_submission_age.value
            )
        if self.canvas_course_id_copying_enabled.is_just:
            res["CANVAS_COURSE_ID_COPYING_ENABLED"] = to_dict(
                self.canvas_course_id_copying_enabled.value
            )
        if self.editor_enabled_for_teachers.is_just:
            res["EDITOR_ENABLED_FOR_TEACHERS"] = to_dict(
                self.editor_enabled_for_teachers.value
            )
        if self.test_submission_copying_on_import_enabled.is_just:
            res["TEST_SUBMISSION_COPYING_ON_IMPORT_ENABLED"] = to_dict(
                self.test_submission_copying_on_import_enabled.value
            )
        if self.new_auto_test_diff_viewer_enabled.is_just:
            res["NEW_AUTO_TEST_DIFF_VIEWER_ENABLED"] = to_dict(
                self.new_auto_test_diff_viewer_enabled.value
            )
        if self.staged_assignment_importer_enabled.is_just:
            res["STAGED_ASSIGNMENT_IMPORTER_ENABLED"] = to_dict(
                self.staged_assignment_importer_enabled.value
            )
        if self.sections_in_submission_list_enabled.is_just:
            res["SECTIONS_IN_SUBMISSION_LIST_ENABLED"] = to_dict(
                self.sections_in_submission_list_enabled.value
            )
        if self.github_template_repo_enabled.is_just:
            res["GITHUB_TEMPLATE_REPO_ENABLED"] = to_dict(
                self.github_template_repo_enabled.value
            )
        if self.community_library.is_just:
            res["COMMUNITY_LIBRARY"] = to_dict(self.community_library.value)
        if self.community_library_publishing.is_just:
            res["COMMUNITY_LIBRARY_PUBLISHING"] = to_dict(
                self.community_library_publishing.value
            )
        if self.plagiarism_pdf_export_enabled.is_just:
            res["PLAGIARISM_PDF_EXPORT_ENABLED"] = to_dict(
                self.plagiarism_pdf_export_enabled.value
            )
        if self.plagiarism_bulk_export_enabled.is_just:
            res["PLAGIARISM_BULK_EXPORT_ENABLED"] = to_dict(
                self.plagiarism_bulk_export_enabled.value
            )
        if self.plagiarism_bulk_export_max_cases.is_just:
            res["PLAGIARISM_BULK_EXPORT_MAX_CASES"] = to_dict(
                self.plagiarism_bulk_export_max_cases.value
            )
        if self.quality_comments_in_code_editor.is_just:
            res["QUALITY_COMMENTS_IN_CODE_EDITOR"] = to_dict(
                self.quality_comments_in_code_editor.value
            )
        if self.sso_infer_global_staff_role.is_just:
            res["SSO_INFER_GLOBAL_STAFF_ROLE"] = to_dict(
                self.sso_infer_global_staff_role.value
            )
        return res

    @classmethod
    def from_dict(
        cls: t.Type["FrontendSiteSettings"], d: t.Dict[str, t.Any]
    ) -> "FrontendSiteSettings":
        parsed = cls.data_parser.try_parse(d)

        res = cls(
            auto_test_max_time_command=parsed.AUTO_TEST_MAX_TIME_COMMAND,
            auto_test_io_test_message=parsed.AUTO_TEST_IO_TEST_MESSAGE,
            auto_test_io_test_sub_message=parsed.AUTO_TEST_IO_TEST_SUB_MESSAGE,
            auto_test_run_program_message=parsed.AUTO_TEST_RUN_PROGRAM_MESSAGE,
            auto_test_capture_points_message=parsed.AUTO_TEST_CAPTURE_POINTS_MESSAGE,
            auto_test_checkpoint_message=parsed.AUTO_TEST_CHECKPOINT_MESSAGE,
            auto_test_unit_test_message=parsed.AUTO_TEST_UNIT_TEST_MESSAGE,
            auto_test_code_quality_message=parsed.AUTO_TEST_CODE_QUALITY_MESSAGE,
            new_auto_test_current_initial_build_ids=parsed.NEW_AUTO_TEST_CURRENT_INITIAL_BUILD_IDS,
            new_auto_test_build_max_command_time=parsed.NEW_AUTO_TEST_BUILD_MAX_COMMAND_TIME,
            new_auto_test_test_max_command_time=parsed.NEW_AUTO_TEST_TEST_MAX_COMMAND_TIME,
            exam_login_max_length=parsed.EXAM_LOGIN_MAX_LENGTH,
            login_token_before_time=parsed.LOGIN_TOKEN_BEFORE_TIME,
            reset_token_time=parsed.RESET_TOKEN_TIME,
            site_email=parsed.SITE_EMAIL,
            max_lines=parsed.MAX_LINES,
            notification_poll_time=parsed.NOTIFICATION_POLL_TIME,
            release_message_max_time=parsed.RELEASE_MESSAGE_MAX_TIME,
            max_plagiarism_matches=parsed.MAX_PLAGIARISM_MATCHES,
            auto_test_max_global_setup_time=parsed.AUTO_TEST_MAX_GLOBAL_SETUP_TIME,
            auto_test_max_per_student_setup_time=parsed.AUTO_TEST_MAX_PER_STUDENT_SETUP_TIME,
            assignment_default_grading_scale=parsed.ASSIGNMENT_DEFAULT_GRADING_SCALE,
            assignment_default_grading_scale_points=parsed.ASSIGNMENT_DEFAULT_GRADING_SCALE_POINTS,
            blackboard_zip_upload_enabled=parsed.BLACKBOARD_ZIP_UPLOAD_ENABLED,
            rubrics_enabled=parsed.RUBRICS_ENABLED,
            rubric_enabled_for_teacher_on_submissions_page=parsed.RUBRIC_ENABLED_FOR_TEACHER_ON_SUBMISSIONS_PAGE,
            automatic_lti_role_enabled=parsed.AUTOMATIC_LTI_ROLE_ENABLED,
            lti_enabled=parsed.LTI_ENABLED,
            linters_enabled=parsed.LINTERS_ENABLED,
            incremental_rubric_submission_enabled=parsed.INCREMENTAL_RUBRIC_SUBMISSION_ENABLED,
            register_enabled=parsed.REGISTER_ENABLED,
            groups_enabled=parsed.GROUPS_ENABLED,
            auto_test_enabled=parsed.AUTO_TEST_ENABLED,
            course_register_enabled=parsed.COURSE_REGISTER_ENABLED,
            render_html_enabled=parsed.RENDER_HTML_ENABLED,
            email_students_enabled=parsed.EMAIL_STUDENTS_ENABLED,
            peer_feedback_enabled=parsed.PEER_FEEDBACK_ENABLED,
            at_image_caching_enabled=parsed.AT_IMAGE_CACHING_ENABLED,
            student_payment_enabled=parsed.STUDENT_PAYMENT_ENABLED,
            editor_enabled=parsed.EDITOR_ENABLED,
            new_auto_test_enabled=parsed.NEW_AUTO_TEST_ENABLED,
            server_time_correction_enabled=parsed.SERVER_TIME_CORRECTION_ENABLED,
            metric_gathering_enabled=parsed.METRIC_GATHERING_ENABLED,
            grading_notifications_enabled=parsed.GRADING_NOTIFICATIONS_ENABLED,
            feedback_threads_initially_collapsed=parsed.FEEDBACK_THREADS_INITIALLY_COLLAPSED,
            metric_gathering_time_interval=parsed.METRIC_GATHERING_TIME_INTERVAL,
            metric_gathering_event_interval=parsed.METRIC_GATHERING_EVENT_INTERVAL,
            metric_event_buffer_size=parsed.METRIC_EVENT_BUFFER_SIZE,
            metric_evaluation_time_limit=parsed.METRIC_EVALUATION_TIME_LIMIT,
            metric_evaluation_time_chunk_size=parsed.METRIC_EVALUATION_TIME_CHUNK_SIZE,
            metric_gathering_expressions=parsed.METRIC_GATHERING_EXPRESSIONS,
            server_time_diff_tolerance=parsed.SERVER_TIME_DIFF_TOLERANCE,
            server_time_sync_interval=parsed.SERVER_TIME_SYNC_INTERVAL,
            is_admin_permission_enabled=parsed.IS_ADMIN_PERMISSION_ENABLED,
            tour_polling_interval=parsed.TOUR_POLLING_INTERVAL,
            find_element_interval=parsed.FIND_ELEMENT_INTERVAL,
            find_element_max_tries=parsed.FIND_ELEMENT_MAX_TRIES,
            tour_configurations=parsed.TOUR_CONFIGURATIONS,
            assignment_percentage_decimals=parsed.ASSIGNMENT_PERCENTAGE_DECIMALS,
            assignment_point_decimals=parsed.ASSIGNMENT_POINT_DECIMALS,
            output_viewer_animation_limit_lines_count=parsed.OUTPUT_VIEWER_ANIMATION_LIMIT_LINES_COUNT,
            lti_lock_date_copying_enabled=parsed.LTI_LOCK_DATE_COPYING_ENABLED,
            assignment_max_points_enabled=parsed.ASSIGNMENT_MAX_POINTS_ENABLED,
            course_gradebook_enabled=parsed.COURSE_GRADEBOOK_ENABLED,
            assignment_description_enabled=parsed.ASSIGNMENT_DESCRIPTION_ENABLED,
            course_gradebook_render_warning_size=parsed.COURSE_GRADEBOOK_RENDER_WARNING_SIZE,
            course_bulk_register_enabled=parsed.COURSE_BULK_REGISTER_ENABLED,
            csv_large_file_limit=parsed.CSV_LARGE_FILE_LIMIT,
            csv_too_many_errors_limit=parsed.CSV_TOO_MANY_ERRORS_LIMIT,
            new_auto_test_copying_enabled=parsed.NEW_AUTO_TEST_COPYING_ENABLED,
            assignment_grading_scale_points_enabled=parsed.ASSIGNMENT_GRADING_SCALE_POINTS_ENABLED,
            new_auto_test_old_submission_age=parsed.NEW_AUTO_TEST_OLD_SUBMISSION_AGE,
            canvas_course_id_copying_enabled=parsed.CANVAS_COURSE_ID_COPYING_ENABLED,
            editor_enabled_for_teachers=parsed.EDITOR_ENABLED_FOR_TEACHERS,
            test_submission_copying_on_import_enabled=parsed.TEST_SUBMISSION_COPYING_ON_IMPORT_ENABLED,
            new_auto_test_diff_viewer_enabled=parsed.NEW_AUTO_TEST_DIFF_VIEWER_ENABLED,
            staged_assignment_importer_enabled=parsed.STAGED_ASSIGNMENT_IMPORTER_ENABLED,
            sections_in_submission_list_enabled=parsed.SECTIONS_IN_SUBMISSION_LIST_ENABLED,
            github_template_repo_enabled=parsed.GITHUB_TEMPLATE_REPO_ENABLED,
            community_library=parsed.COMMUNITY_LIBRARY,
            community_library_publishing=parsed.COMMUNITY_LIBRARY_PUBLISHING,
            plagiarism_pdf_export_enabled=parsed.PLAGIARISM_PDF_EXPORT_ENABLED,
            plagiarism_bulk_export_enabled=parsed.PLAGIARISM_BULK_EXPORT_ENABLED,
            plagiarism_bulk_export_max_cases=parsed.PLAGIARISM_BULK_EXPORT_MAX_CASES,
            quality_comments_in_code_editor=parsed.QUALITY_COMMENTS_IN_CODE_EDITOR,
            sso_infer_global_staff_role=parsed.SSO_INFER_GLOBAL_STAFF_ROLE,
        )
        res.raw_data = d
        return res
