import { useEffect } from 'react'
import { useTopicWorkspace } from '@/hooks/useTopicWorkspace'
import { StatusBar } from './StatusBar'
import { ActivityFeed } from './ActivityFeed'
import { PlanReview } from './PlanReview'
import { ReportView } from './ReportView'
import { MonitorPanel } from './MonitorPanel'
import { CardSkeleton } from '@/components/ui/Skeleton'
import { markTopicVisited } from '@/lib/storage'

export function TopicWorkspace({ topicId }: { topicId: string }) {
  const ws = useTopicWorkspace(topicId)

  useEffect(() => {
    markTopicVisited(topicId)
  }, [topicId])

  if (ws.loading || !ws.topic) {
    return (
      <div className="space-y-4">
        <CardSkeleton />
        <div className="grid gap-4 lg:grid-cols-2">
          <CardSkeleton />
          <CardSkeleton />
        </div>
      </div>
    )
  }

  const showPlan =
    ws.topic.state === 'planned_awaiting_review' ||
    ws.artifacts.introMd !== null ||
    ws.artifacts.parsed !== null

  const showReport =
    ws.topic.state === 'delivering' ||
    ws.topic.state === 'reported' ||
    ws.artifacts.reportMd !== null

  const showMonitor = ws.topic.state === 'reported'

  return (
    <div className="space-y-4">
      <StatusBar
        topic={ws.topic}
        sseStatus={ws.sseStatus}
        onProceed={() => void ws.proceed()}
        onCancel={() => void ws.cancel()}
        actionLoading={ws.actionLoading}
      />

      {ws.sseError && (
        <div className="rounded-lg border border-warning/30 bg-warning/10 px-4 py-2 text-xs text-warning">
          Stream: {ws.sseError} — reconnecting automatically
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-5">
        <div className="lg:col-span-2">
          <ActivityFeed events={ws.events} />
        </div>
        <div className="lg:col-span-3 space-y-4">
          <PlanReview
            introMd={ws.artifacts.introMd}
            parsed={ws.artifacts.parsed}
            loading={ws.artifactLoading.introMd || ws.artifactLoading.parsed}
            visible={showPlan}
          />
          <ReportView
            reportMd={ws.artifacts.reportMd}
            report={ws.artifacts.report}
            news={ws.artifacts.news}
            loading={
              ws.artifactLoading.reportMd ||
              ws.artifactLoading.report ||
              ws.artifactLoading.news
            }
            visible={showReport}
          />
          <MonitorPanel
            monitor={ws.monitor}
            deltas={ws.deltas}
            selectedDelta={ws.selectedDelta}
            deltaDetail={ws.deltaDetail}
            onEnable={(h) => void ws.enableMonitor(h)}
            onDisable={() => void ws.disableMonitor()}
            onRefresh={() => void ws.refresh()}
            onOpenDelta={(s) => void ws.openDelta(s)}
            onCloseDelta={ws.closeDelta}
            actionLoading={ws.actionLoading}
            visible={showMonitor}
          />
        </div>
      </div>
    </div>
  )
}
