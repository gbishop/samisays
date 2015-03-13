**Description**

Captures keys and gives audio cues to control the creation of a story.  Allows user to create, navigate, and delete the clips of a story.  Also enables user to enter the module for inserting sound effects.  Exiting this module returns the user to managing his or her stories.

**Full Story Playback**

Because we wanted all sounds to be interruptible and we wanted the interrupt to put the user at the specific clip that was interrupted, threading is required for full story playback.  StoryPlayback loops through the clips playing them and busy-waiting in between.  If the user presses a valid key, a flag is set by AuiStoryCreation that is caught by the busy-waiting thread and causes it to exit, leaving the current clip pointer at the correct position.

**Teacher Template Mode**

The AuiStoryCreation operates in both teacher template mode and student story mode as specified by the teacherMode flag.  Teacher mode can only be accessed using the “Teacher Template” button on GuiStart.  In teacher mode, stories are called templates and breaks can be inserted between clips.  The template can be assigned as stories to students.  The clips between breaks are combined into a single clip and are locked so that students may not alter them.