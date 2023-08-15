"""The module that defines the ``SiteSettingInput`` model.

SPDX-License-Identifier: AGPL-3.0-only OR BSD-3-Clause-Clear
"""

import typing as t
from dataclasses import dataclass, field

import cg_request_args as rqa

from ..parsers import ParserFor, make_union
from ..utils import to_dict
from .assignment_default_grading_scale_points_setting import (
    AssignmentDefaultGradingScalePointsSetting,
)
from .assignment_default_grading_scale_setting import (
    AssignmentDefaultGradingScaleSetting,
)
from .assignment_description_enabled_setting import (
    AssignmentDescriptionEnabledSetting,
)
from .assignment_grading_scale_points_enabled_setting import (
    AssignmentGradingScalePointsEnabledSetting,
)
from .assignment_max_points_enabled_setting import (
    AssignmentMaxPointsEnabledSetting,
)
from .assignment_percentage_decimals_setting import (
    AssignmentPercentageDecimalsSetting,
)
from .assignment_point_decimals_setting import AssignmentPointDecimalsSetting
from .at_image_caching_enabled_setting import AtImageCachingEnabledSetting
from .auto_test_capture_points_message_setting import (
    AutoTestCapturePointsMessageSetting,
)
from .auto_test_checkpoint_message_setting import (
    AutoTestCheckpointMessageSetting,
)
from .auto_test_code_quality_message_setting import (
    AutoTestCodeQualityMessageSetting,
)
from .auto_test_enabled_setting import AutoTestEnabledSetting
from .auto_test_heartbeat_interval_setting import (
    AutoTestHeartbeatIntervalSetting,
)
from .auto_test_heartbeat_max_missed_setting import (
    AutoTestHeartbeatMaxMissedSetting,
)
from .auto_test_io_test_message_setting import AutoTestIoTestMessageSetting
from .auto_test_io_test_sub_message_setting import (
    AutoTestIoTestSubMessageSetting,
)
from .auto_test_max_concurrent_batch_runs_setting import (
    AutoTestMaxConcurrentBatchRunsSetting,
)
from .auto_test_max_global_setup_time_setting import (
    AutoTestMaxGlobalSetupTimeSetting,
)
from .auto_test_max_jobs_per_runner_setting import (
    AutoTestMaxJobsPerRunnerSetting,
)
from .auto_test_max_per_student_setup_time_setting import (
    AutoTestMaxPerStudentSetupTimeSetting,
)
from .auto_test_max_result_not_started_setting import (
    AutoTestMaxResultNotStartedSetting,
)
from .auto_test_max_time_command_setting import AutoTestMaxTimeCommandSetting
from .auto_test_max_unit_test_metadata_length_setting import (
    AutoTestMaxUnitTestMetadataLengthSetting,
)
from .auto_test_run_program_message_setting import (
    AutoTestRunProgramMessageSetting,
)
from .auto_test_unit_test_message_setting import AutoTestUnitTestMessageSetting
from .automatic_lti1p3_assignment_import_setting import (
    AutomaticLti1p3AssignmentImportSetting,
)
from .automatic_lti_role_enabled_setting import AutomaticLtiRoleEnabledSetting
from .blackboard_zip_upload_enabled_setting import (
    BlackboardZipUploadEnabledSetting,
)
from .canvas_course_id_copying_enabled_setting import (
    CanvasCourseIdCopyingEnabledSetting,
)
from .community_library_publishing_setting import (
    CommunityLibraryPublishingSetting,
)
from .community_library_setting import CommunityLibrarySetting
from .course_bulk_register_enabled_setting import (
    CourseBulkRegisterEnabledSetting,
)
from .course_gradebook_enabled_setting import CourseGradebookEnabledSetting
from .course_gradebook_render_warning_size_setting import (
    CourseGradebookRenderWarningSizeSetting,
)
from .course_register_enabled_setting import CourseRegisterEnabledSetting
from .csv_large_file_limit_setting import CsvLargeFileLimitSetting
from .csv_too_many_errors_limit_setting import CsvTooManyErrorsLimitSetting
from .editor_enabled_for_teachers_setting import (
    EditorEnabledForTeachersSetting,
)
from .editor_enabled_setting import EditorEnabledSetting
from .email_students_enabled_setting import EmailStudentsEnabledSetting
from .exam_login_max_length_setting import ExamLoginMaxLengthSetting
from .feedback_threads_initially_collapsed_setting import (
    FeedbackThreadsInitiallyCollapsedSetting,
)
from .find_element_interval_setting import FindElementIntervalSetting
from .find_element_max_tries_setting import FindElementMaxTriesSetting
from .github_template_repo_enabled_setting import (
    GithubTemplateRepoEnabledSetting,
)
from .grading_notifications_enabled_setting import (
    GradingNotificationsEnabledSetting,
)
from .groups_enabled_setting import GroupsEnabledSetting
from .incremental_rubric_submission_enabled_setting import (
    IncrementalRubricSubmissionEnabledSetting,
)
from .is_admin_permission_enabled_setting import (
    IsAdminPermissionEnabledSetting,
)
from .jwt_access_token_expires_setting import JwtAccessTokenExpiresSetting
from .linters_enabled_setting import LintersEnabledSetting
from .login_token_before_time_setting import LoginTokenBeforeTimeSetting
from .lti1p3_parse_most_privileged_role_setting import (
    Lti1p3ParseMostPrivilegedRoleSetting,
)
from .lti1p3_system_role_from_context_role_setting import (
    Lti1p3SystemRoleFromContextRoleSetting,
)
from .lti_enabled_setting import LtiEnabledSetting
from .lti_lock_date_copying_enabled_setting import (
    LtiLockDateCopyingEnabledSetting,
)
from .lti_unset_deadline_lock_date_enabled_setting import (
    LtiUnsetDeadlineLockDateEnabledSetting,
)
from .max_document_update_size_setting import MaxDocumentUpdateSizeSetting
from .max_dynamo_file_size_setting import MaxDynamoFileSizeSetting
from .max_dynamo_submission_size_setting import MaxDynamoSubmissionSizeSetting
from .max_file_size_setting import MaxFileSizeSetting
from .max_large_upload_size_setting import MaxLargeUploadSizeSetting
from .max_lines_setting import MaxLinesSetting
from .max_mirror_file_age_setting import MaxMirrorFileAgeSetting
from .max_normal_upload_size_setting import MaxNormalUploadSizeSetting
from .max_number_of_files_setting import MaxNumberOfFilesSetting
from .max_plagiarism_matches_setting import MaxPlagiarismMatchesSetting
from .max_user_setting_amount_setting import MaxUserSettingAmountSetting
from .metric_evaluation_time_chunk_size_setting import (
    MetricEvaluationTimeChunkSizeSetting,
)
from .metric_evaluation_time_limit_setting import (
    MetricEvaluationTimeLimitSetting,
)
from .metric_event_buffer_size_setting import MetricEventBufferSizeSetting
from .metric_gathering_enabled_setting import MetricGatheringEnabledSetting
from .metric_gathering_event_interval_setting import (
    MetricGatheringEventIntervalSetting,
)
from .metric_gathering_expressions_setting import (
    MetricGatheringExpressionsSetting,
)
from .metric_gathering_time_interval_setting import (
    MetricGatheringTimeIntervalSetting,
)
from .min_password_score_setting import MinPasswordScoreSetting
from .new_auto_test_allowed_initial_build_ids_setting import (
    NewAutoTestAllowedInitialBuildIdsSetting,
)
from .new_auto_test_build_max_command_time_setting import (
    NewAutoTestBuildMaxCommandTimeSetting,
)
from .new_auto_test_build_output_limit_setting import (
    NewAutoTestBuildOutputLimitSetting,
)
from .new_auto_test_copying_enabled_setting import (
    NewAutoTestCopyingEnabledSetting,
)
from .new_auto_test_current_initial_build_ids_setting import (
    NewAutoTestCurrentInitialBuildIdsSetting,
)
from .new_auto_test_diff_viewer_enabled_setting import (
    NewAutoTestDiffViewerEnabledSetting,
)
from .new_auto_test_enabled_setting import NewAutoTestEnabledSetting
from .new_auto_test_initial_build_id_setting import (
    NewAutoTestInitialBuildIdSetting,
)
from .new_auto_test_max_dynamodb_size_setting import (
    NewAutoTestMaxDynamodbSizeSetting,
)
from .new_auto_test_max_file_size_setting import NewAutoTestMaxFileSizeSetting
from .new_auto_test_max_storage_size_setting import (
    NewAutoTestMaxStorageSizeSetting,
)
from .new_auto_test_old_submission_age_setting import (
    NewAutoTestOldSubmissionAgeSetting,
)
from .new_auto_test_test_max_command_time_setting import (
    NewAutoTestTestMaxCommandTimeSetting,
)
from .new_auto_test_test_output_limit_setting import (
    NewAutoTestTestOutputLimitSetting,
)
from .notification_poll_time_setting import NotificationPollTimeSetting
from .output_viewer_animation_limit_lines_count_setting import (
    OutputViewerAnimationLimitLinesCountSetting,
)
from .peer_feedback_enabled_setting import PeerFeedbackEnabledSetting
from .plagiarism_bulk_export_enabled_setting import (
    PlagiarismBulkExportEnabledSetting,
)
from .plagiarism_bulk_export_max_cases_setting import (
    PlagiarismBulkExportMaxCasesSetting,
)
from .plagiarism_pdf_export_enabled_setting import (
    PlagiarismPdfExportEnabledSetting,
)
from .quality_comments_in_code_editor_setting import (
    QualityCommentsInCodeEditorSetting,
)
from .register_enabled_setting import RegisterEnabledSetting
from .release_message_max_time_setting import ReleaseMessageMaxTimeSetting
from .render_html_enabled_setting import RenderHtmlEnabledSetting
from .reset_token_time_setting import ResetTokenTimeSetting
from .rubric_enabled_for_teacher_on_submissions_page_setting import (
    RubricEnabledForTeacherOnSubmissionsPageSetting,
)
from .rubrics_enabled_setting import RubricsEnabledSetting
from .sections_in_submission_list_enabled_setting import (
    SectionsInSubmissionListEnabledSetting,
)
from .send_registration_email_setting import SendRegistrationEmailSetting
from .server_time_correction_enabled_setting import (
    ServerTimeCorrectionEnabledSetting,
)
from .server_time_diff_tolerance_setting import ServerTimeDiffToleranceSetting
from .server_time_sync_interval_setting import ServerTimeSyncIntervalSetting
from .setting_token_time_setting import SettingTokenTimeSetting
from .site_email_setting import SiteEmailSetting
from .sso_infer_global_staff_role_setting import SsoInferGlobalStaffRoleSetting
from .sso_username_decollision_enabled_setting import (
    SsoUsernameDecollisionEnabledSetting,
)
from .staged_assignment_importer_enabled_setting import (
    StagedAssignmentImporterEnabledSetting,
)
from .student_payment_enabled_setting import StudentPaymentEnabledSetting
from .test_submission_copying_on_import_enabled_setting import (
    TestSubmissionCopyingOnImportEnabledSetting,
)
from .tour_configurations_setting import TourConfigurationsSetting
from .tour_polling_interval_setting import TourPollingIntervalSetting

SiteSettingInput = t.Union[
    AutoTestMaxTimeCommandSetting,
    AutoTestHeartbeatIntervalSetting,
    AutoTestHeartbeatMaxMissedSetting,
    AutoTestMaxJobsPerRunnerSetting,
    AutoTestMaxConcurrentBatchRunsSetting,
    AutoTestIoTestMessageSetting,
    AutoTestIoTestSubMessageSetting,
    AutoTestRunProgramMessageSetting,
    AutoTestCapturePointsMessageSetting,
    AutoTestCheckpointMessageSetting,
    AutoTestUnitTestMessageSetting,
    AutoTestCodeQualityMessageSetting,
    AutoTestMaxResultNotStartedSetting,
    AutoTestMaxUnitTestMetadataLengthSetting,
    NewAutoTestMaxDynamodbSizeSetting,
    NewAutoTestMaxStorageSizeSetting,
    NewAutoTestMaxFileSizeSetting,
    NewAutoTestBuildOutputLimitSetting,
    NewAutoTestTestOutputLimitSetting,
    NewAutoTestCurrentInitialBuildIdsSetting,
    NewAutoTestAllowedInitialBuildIdsSetting,
    NewAutoTestInitialBuildIdSetting,
    NewAutoTestBuildMaxCommandTimeSetting,
    NewAutoTestTestMaxCommandTimeSetting,
    ExamLoginMaxLengthSetting,
    LoginTokenBeforeTimeSetting,
    MinPasswordScoreSetting,
    ResetTokenTimeSetting,
    SettingTokenTimeSetting,
    SiteEmailSetting,
    MaxNumberOfFilesSetting,
    MaxLargeUploadSizeSetting,
    MaxNormalUploadSizeSetting,
    MaxDynamoSubmissionSizeSetting,
    MaxFileSizeSetting,
    MaxDynamoFileSizeSetting,
    MaxDocumentUpdateSizeSetting,
    JwtAccessTokenExpiresSetting,
    MaxLinesSetting,
    NotificationPollTimeSetting,
    ReleaseMessageMaxTimeSetting,
    MaxPlagiarismMatchesSetting,
    MaxMirrorFileAgeSetting,
    AutoTestMaxGlobalSetupTimeSetting,
    AutoTestMaxPerStudentSetupTimeSetting,
    AssignmentDefaultGradingScaleSetting,
    AssignmentDefaultGradingScalePointsSetting,
    BlackboardZipUploadEnabledSetting,
    RubricsEnabledSetting,
    RubricEnabledForTeacherOnSubmissionsPageSetting,
    AutomaticLtiRoleEnabledSetting,
    LtiEnabledSetting,
    LintersEnabledSetting,
    IncrementalRubricSubmissionEnabledSetting,
    RegisterEnabledSetting,
    GroupsEnabledSetting,
    AutoTestEnabledSetting,
    CourseRegisterEnabledSetting,
    RenderHtmlEnabledSetting,
    EmailStudentsEnabledSetting,
    PeerFeedbackEnabledSetting,
    AtImageCachingEnabledSetting,
    StudentPaymentEnabledSetting,
    EditorEnabledSetting,
    NewAutoTestEnabledSetting,
    ServerTimeCorrectionEnabledSetting,
    MetricGatheringEnabledSetting,
    GradingNotificationsEnabledSetting,
    SsoUsernameDecollisionEnabledSetting,
    FeedbackThreadsInitiallyCollapsedSetting,
    MaxUserSettingAmountSetting,
    SendRegistrationEmailSetting,
    MetricGatheringTimeIntervalSetting,
    MetricGatheringEventIntervalSetting,
    MetricEventBufferSizeSetting,
    MetricEvaluationTimeLimitSetting,
    MetricEvaluationTimeChunkSizeSetting,
    MetricGatheringExpressionsSetting,
    ServerTimeDiffToleranceSetting,
    ServerTimeSyncIntervalSetting,
    IsAdminPermissionEnabledSetting,
    TourPollingIntervalSetting,
    FindElementIntervalSetting,
    FindElementMaxTriesSetting,
    TourConfigurationsSetting,
    AutomaticLti1p3AssignmentImportSetting,
    AssignmentPercentageDecimalsSetting,
    AssignmentPointDecimalsSetting,
    OutputViewerAnimationLimitLinesCountSetting,
    LtiLockDateCopyingEnabledSetting,
    AssignmentMaxPointsEnabledSetting,
    CourseGradebookEnabledSetting,
    AssignmentDescriptionEnabledSetting,
    CourseGradebookRenderWarningSizeSetting,
    CourseBulkRegisterEnabledSetting,
    CsvLargeFileLimitSetting,
    CsvTooManyErrorsLimitSetting,
    NewAutoTestCopyingEnabledSetting,
    AssignmentGradingScalePointsEnabledSetting,
    NewAutoTestOldSubmissionAgeSetting,
    CanvasCourseIdCopyingEnabledSetting,
    EditorEnabledForTeachersSetting,
    TestSubmissionCopyingOnImportEnabledSetting,
    NewAutoTestDiffViewerEnabledSetting,
    StagedAssignmentImporterEnabledSetting,
    LtiUnsetDeadlineLockDateEnabledSetting,
    SectionsInSubmissionListEnabledSetting,
    GithubTemplateRepoEnabledSetting,
    CommunityLibrarySetting,
    CommunityLibraryPublishingSetting,
    Lti1p3SystemRoleFromContextRoleSetting,
    Lti1p3ParseMostPrivilegedRoleSetting,
    PlagiarismPdfExportEnabledSetting,
    PlagiarismBulkExportEnabledSetting,
    PlagiarismBulkExportMaxCasesSetting,
    QualityCommentsInCodeEditorSetting,
    SsoInferGlobalStaffRoleSetting,
]
SiteSettingInputParser = rqa.Lazy(
    lambda: make_union(
        ParserFor.make(AutoTestMaxTimeCommandSetting),
        ParserFor.make(AutoTestHeartbeatIntervalSetting),
        ParserFor.make(AutoTestHeartbeatMaxMissedSetting),
        ParserFor.make(AutoTestMaxJobsPerRunnerSetting),
        ParserFor.make(AutoTestMaxConcurrentBatchRunsSetting),
        ParserFor.make(AutoTestIoTestMessageSetting),
        ParserFor.make(AutoTestIoTestSubMessageSetting),
        ParserFor.make(AutoTestRunProgramMessageSetting),
        ParserFor.make(AutoTestCapturePointsMessageSetting),
        ParserFor.make(AutoTestCheckpointMessageSetting),
        ParserFor.make(AutoTestUnitTestMessageSetting),
        ParserFor.make(AutoTestCodeQualityMessageSetting),
        ParserFor.make(AutoTestMaxResultNotStartedSetting),
        ParserFor.make(AutoTestMaxUnitTestMetadataLengthSetting),
        ParserFor.make(NewAutoTestMaxDynamodbSizeSetting),
        ParserFor.make(NewAutoTestMaxStorageSizeSetting),
        ParserFor.make(NewAutoTestMaxFileSizeSetting),
        ParserFor.make(NewAutoTestBuildOutputLimitSetting),
        ParserFor.make(NewAutoTestTestOutputLimitSetting),
        ParserFor.make(NewAutoTestCurrentInitialBuildIdsSetting),
        ParserFor.make(NewAutoTestAllowedInitialBuildIdsSetting),
        ParserFor.make(NewAutoTestInitialBuildIdSetting),
        ParserFor.make(NewAutoTestBuildMaxCommandTimeSetting),
        ParserFor.make(NewAutoTestTestMaxCommandTimeSetting),
        ParserFor.make(ExamLoginMaxLengthSetting),
        ParserFor.make(LoginTokenBeforeTimeSetting),
        ParserFor.make(MinPasswordScoreSetting),
        ParserFor.make(ResetTokenTimeSetting),
        ParserFor.make(SettingTokenTimeSetting),
        ParserFor.make(SiteEmailSetting),
        ParserFor.make(MaxNumberOfFilesSetting),
        ParserFor.make(MaxLargeUploadSizeSetting),
        ParserFor.make(MaxNormalUploadSizeSetting),
        ParserFor.make(MaxDynamoSubmissionSizeSetting),
        ParserFor.make(MaxFileSizeSetting),
        ParserFor.make(MaxDynamoFileSizeSetting),
        ParserFor.make(MaxDocumentUpdateSizeSetting),
        ParserFor.make(JwtAccessTokenExpiresSetting),
        ParserFor.make(MaxLinesSetting),
        ParserFor.make(NotificationPollTimeSetting),
        ParserFor.make(ReleaseMessageMaxTimeSetting),
        ParserFor.make(MaxPlagiarismMatchesSetting),
        ParserFor.make(MaxMirrorFileAgeSetting),
        ParserFor.make(AutoTestMaxGlobalSetupTimeSetting),
        ParserFor.make(AutoTestMaxPerStudentSetupTimeSetting),
        ParserFor.make(AssignmentDefaultGradingScaleSetting),
        ParserFor.make(AssignmentDefaultGradingScalePointsSetting),
        ParserFor.make(BlackboardZipUploadEnabledSetting),
        ParserFor.make(RubricsEnabledSetting),
        ParserFor.make(RubricEnabledForTeacherOnSubmissionsPageSetting),
        ParserFor.make(AutomaticLtiRoleEnabledSetting),
        ParserFor.make(LtiEnabledSetting),
        ParserFor.make(LintersEnabledSetting),
        ParserFor.make(IncrementalRubricSubmissionEnabledSetting),
        ParserFor.make(RegisterEnabledSetting),
        ParserFor.make(GroupsEnabledSetting),
        ParserFor.make(AutoTestEnabledSetting),
        ParserFor.make(CourseRegisterEnabledSetting),
        ParserFor.make(RenderHtmlEnabledSetting),
        ParserFor.make(EmailStudentsEnabledSetting),
        ParserFor.make(PeerFeedbackEnabledSetting),
        ParserFor.make(AtImageCachingEnabledSetting),
        ParserFor.make(StudentPaymentEnabledSetting),
        ParserFor.make(EditorEnabledSetting),
        ParserFor.make(NewAutoTestEnabledSetting),
        ParserFor.make(ServerTimeCorrectionEnabledSetting),
        ParserFor.make(MetricGatheringEnabledSetting),
        ParserFor.make(GradingNotificationsEnabledSetting),
        ParserFor.make(SsoUsernameDecollisionEnabledSetting),
        ParserFor.make(FeedbackThreadsInitiallyCollapsedSetting),
        ParserFor.make(MaxUserSettingAmountSetting),
        ParserFor.make(SendRegistrationEmailSetting),
        ParserFor.make(MetricGatheringTimeIntervalSetting),
        ParserFor.make(MetricGatheringEventIntervalSetting),
        ParserFor.make(MetricEventBufferSizeSetting),
        ParserFor.make(MetricEvaluationTimeLimitSetting),
        ParserFor.make(MetricEvaluationTimeChunkSizeSetting),
        ParserFor.make(MetricGatheringExpressionsSetting),
        ParserFor.make(ServerTimeDiffToleranceSetting),
        ParserFor.make(ServerTimeSyncIntervalSetting),
        ParserFor.make(IsAdminPermissionEnabledSetting),
        ParserFor.make(TourPollingIntervalSetting),
        ParserFor.make(FindElementIntervalSetting),
        ParserFor.make(FindElementMaxTriesSetting),
        ParserFor.make(TourConfigurationsSetting),
        ParserFor.make(AutomaticLti1p3AssignmentImportSetting),
        ParserFor.make(AssignmentPercentageDecimalsSetting),
        ParserFor.make(AssignmentPointDecimalsSetting),
        ParserFor.make(OutputViewerAnimationLimitLinesCountSetting),
        ParserFor.make(LtiLockDateCopyingEnabledSetting),
        ParserFor.make(AssignmentMaxPointsEnabledSetting),
        ParserFor.make(CourseGradebookEnabledSetting),
        ParserFor.make(AssignmentDescriptionEnabledSetting),
        ParserFor.make(CourseGradebookRenderWarningSizeSetting),
        ParserFor.make(CourseBulkRegisterEnabledSetting),
        ParserFor.make(CsvLargeFileLimitSetting),
        ParserFor.make(CsvTooManyErrorsLimitSetting),
        ParserFor.make(NewAutoTestCopyingEnabledSetting),
        ParserFor.make(AssignmentGradingScalePointsEnabledSetting),
        ParserFor.make(NewAutoTestOldSubmissionAgeSetting),
        ParserFor.make(CanvasCourseIdCopyingEnabledSetting),
        ParserFor.make(EditorEnabledForTeachersSetting),
        ParserFor.make(TestSubmissionCopyingOnImportEnabledSetting),
        ParserFor.make(NewAutoTestDiffViewerEnabledSetting),
        ParserFor.make(StagedAssignmentImporterEnabledSetting),
        ParserFor.make(LtiUnsetDeadlineLockDateEnabledSetting),
        ParserFor.make(SectionsInSubmissionListEnabledSetting),
        ParserFor.make(GithubTemplateRepoEnabledSetting),
        ParserFor.make(CommunityLibrarySetting),
        ParserFor.make(CommunityLibraryPublishingSetting),
        ParserFor.make(Lti1p3SystemRoleFromContextRoleSetting),
        ParserFor.make(Lti1p3ParseMostPrivilegedRoleSetting),
        ParserFor.make(PlagiarismPdfExportEnabledSetting),
        ParserFor.make(PlagiarismBulkExportEnabledSetting),
        ParserFor.make(PlagiarismBulkExportMaxCasesSetting),
        ParserFor.make(QualityCommentsInCodeEditorSetting),
        ParserFor.make(SsoInferGlobalStaffRoleSetting),
    ),
)
