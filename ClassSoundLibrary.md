**Description**

This class mirrors the structure of the Sound Library stored in the file system, providing support for the AuiInsertSound class during story creation. It keeps track of the different categories and the sounds within each category.

The structure can be traversed easily with navigation methods.  A sound manipulation
category is also supported through the SoundEffects class.  A trashcan is supported through the Story class.

**Sound Library Organization**

The sound library is stored in the file system in a directory specified by SOUND\_LIB.  All directories in SOUND\_LIB are treated as sound categories and the directory names are used as the category name.  The sound files (wav, mp3, ogg, aiff, midi) in each directory are listed as sounds in those categories and the filename (as well as the sound itself) are used to identify each sound.

**Organizing Library (Importing sounds, etc.)**

The primary interface to the sound library is the file system.  Advanced users can make new categories by adding directories and input sounds by copy and pasting sound files into the directories.  Sami Says includes a simple GUI for organizing the assigned (prioritized) sounds, however.  See GuiPrioritize for more info.

**Special Categories**

Special categories are “assigned sounds”, “sound manipulations” and “trashcan”.  “Assigned sounds” is the folder made made by the GuiPrioritize class.  It is always placed as the first category.  Unlike “assigned sounds”, the other two special categories are not stored in the file system and are only “virtual” categories.  Sound manipulations are created by the SoundEffects class and the trashcan is part of the Story class.  The Sound Library tricks the AuiInsertSound class into thinking these are normal categories, for the most part at least.  The only difference is that AuiInsertSound checks for sound manipulations when inserting so that it knows whether to replace the current sound clip or delete it.