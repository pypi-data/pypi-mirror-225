tdry
=======

This repo was forked from: https://github.com/pimutils/todoman

---

## Changes made by **rooyca**

#### 1. Shorter Commands

```
cancel: cc
copy: cp
delete: rm
done: do
edit: ed
flush: fl
list: ls
move: mv
new: nw
show: sh
```

#### 2. Add more color to the output.
#### 3. The default `due` date is now `never` (0).
#### 4. Add `percent` selector in the edit command.
#### 5. Add LISTS commands:

- `--newlist` or `-nl` to create a new list.
- `--removelist` or `-rml` to delete a list.
- `--lists` or `-sl` to show all lists.

#### 6. Add `doing` command to focus on a especific task.

- `doing` alone shows the current task.
- `doing <task>` add the task to the doing list.
- `doing --all` or `doing -a` shows all tasks in the doing list.

#### 7. Add `done` command to mark as complete the task that is currently being done.

- `done` alone marks the current task as complete.
- `done --show` or `done -s` shows all completed tasks.
- `done --clear` or `done -c` clears all completed tasks.

#### 8. Add `cancel` command to cancel the task that is currently being done.

#### 9. Add `pause` command to pause the task that is currently being done.

#### 10. Add `resume` command to resume the task that is currently paused.
---

## Bonus

I have created an alias to make the commands even shorter.

```
alias t='todo'
```

## TODO

- [ ] Create a Docker image to run the application.
