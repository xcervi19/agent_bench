import { cn } from '@/lib/utils'

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn('animate-pulse rounded-md bg-surface-overlay', className)}
      aria-hidden
    />
  )
}

export function CardSkeleton() {
  return (
    <div className="rounded-xl border border-border bg-surface-raised p-4 space-y-3">
      <Skeleton className="h-4 w-2/3" />
      <Skeleton className="h-3 w-1/3" />
      <Skeleton className="h-20 w-full" />
    </div>
  )
}
