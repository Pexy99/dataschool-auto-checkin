@echo off
setlocal

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$names = @('DataSchool Check-in','DataSchool Mid-Attendance','DataSchool Check-out'); ^
$result = foreach ($name in $names) { ^
  $task = Get-ScheduledTask -TaskName $name -ErrorAction SilentlyContinue; ^
  if ($null -eq $task) { ^
    [pscustomobject]@{ Name=$name; Start='NOT FOUND'; NextRun='-'; State='-' } ^
  } else { ^
    $info = Get-ScheduledTaskInfo -TaskName $name; ^
    $trigger = @($task.Triggers)[0]; ^
    $start = if ($trigger -and $trigger.StartBoundary) { ([datetime]$trigger.StartBoundary).ToString('HH:mm') } else { '-' }; ^
    $next = if ($info.NextRunTime) { $info.NextRunTime.ToString('yyyy-MM-dd HH:mm') } else { '-' }; ^
    [pscustomobject]@{ Name=$name; Start=$start; NextRun=$next; State=$task.State } ^
  } ^
}; ^
$result | Format-Table -AutoSize"

pause
